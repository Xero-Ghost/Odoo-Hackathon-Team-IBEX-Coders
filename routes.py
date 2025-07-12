import os
from flask import render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import app, db
from models import User, Skill, SkillWanted, SwapRequest, Feedback, AdminMessage
from forms import LoginForm, RegisterForm, ProfileForm, SkillForm, SwapRequestForm, FeedbackForm, AdminMessageForm, SearchForm
from datetime import datetime
import uuid

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth'))

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    login_form = LoginForm()
    register_form = RegisterForm()
    
    # Handle admin login
    if 'admin_login' in request.form:
        admin_password = request.form.get('admin_password')
        if admin_password == 'Admin@123':
            admin_user = User.query.filter_by(is_admin=True).first()
            if admin_user:
                login_user(admin_user)
                return redirect(url_for('admin'))
            else:
                flash('Admin account not found', 'error')
        else:
            flash('Invalid admin password', 'error')
    
    if login_form.validate_on_submit() and 'login' in request.form:
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and check_password_hash(user.password_hash, login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'error')
    
    if register_form.validate_on_submit() and 'register' in request.form:
        if User.query.filter_by(email=register_form.email.data).first():
            flash('Email already registered', 'error')
        else:
            user = User(
                first_name=register_form.first_name.data,
                last_name=register_form.last_name.data,
                email=register_form.email.data,
                location=register_form.location.data,
                password_hash=generate_password_hash(register_form.password.data)
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('dashboard'))
    
    return render_template('auth.html', login_form=login_form, register_form=register_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get recent activity
    recent_requests = SwapRequest.query.filter_by(requested_id=current_user.id, status='pending').limit(5).all()
    completed_swaps = SwapRequest.query.filter(
        ((SwapRequest.requester_id == current_user.id) | (SwapRequest.requested_id == current_user.id)) &
        (SwapRequest.status == 'completed')
    ).limit(5).all()
    
    return render_template('dashboard.html', 
                         recent_requests=recent_requests,
                         completed_swaps=completed_swaps)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile_form = ProfileForm(obj=current_user)
    skill_form = SkillForm()
    
    if profile_form.validate_on_submit() and 'update_profile' in request.form:
        current_user.first_name = profile_form.first_name.data
        current_user.last_name = profile_form.last_name.data
        current_user.email = profile_form.email.data
        current_user.location = profile_form.location.data
        current_user.availability = profile_form.availability.data
        current_user.is_public = profile_form.is_public.data
        
        # Handle profile photo upload
        if profile_form.profile_photo.data:
            file = profile_form.profile_photo.data
            if file and hasattr(file, 'filename') and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Generate unique filename
                filename = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1].lower()
                
                # Create uploads directory if it doesn't exist
                upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                
                file.save(os.path.join(upload_dir, filename))
                current_user.profile_photo = filename
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))
    
    if skill_form.validate_on_submit() and 'add_skill' in request.form:
        skill_type = request.form.get('skill_type')
        if skill_type == 'offered':
            skill = Skill(name=skill_form.name.data, category=skill_form.category.data, user_id=current_user.id)
        else:
            skill = SkillWanted(name=skill_form.name.data, category=skill_form.category.data, user_id=current_user.id)
        
        db.session.add(skill)
        db.session.commit()
        flash('Skill added successfully', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', 
                         profile_form=profile_form, 
                         skill_form=skill_form)

@app.route('/remove_skill/<skill_type>/<int:skill_id>')
@login_required
def remove_skill(skill_type, skill_id):
    if skill_type == 'offered':
        skill = Skill.query.filter_by(id=skill_id, user_id=current_user.id).first()
    else:
        skill = SkillWanted.query.filter_by(id=skill_id, user_id=current_user.id).first()
    
    if skill:
        db.session.delete(skill)
        db.session.commit()
        flash('Skill removed successfully', 'success')
    
    return redirect(url_for('profile'))

@app.route('/browse')
@login_required
def browse():
    search_form = SearchForm()
    
    # Get search parameters
    search_query = request.args.get('search_query', '')
    category = request.args.get('category', '')
    
    # Build query - exclude admins and current user
    query = User.query.filter(User.id != current_user.id, User.is_public == True, User.is_admin == False)
    
    if search_query:
        # Search in skills offered
        skill_users = db.session.query(User.id).join(Skill).filter(
            Skill.name.ilike(f'%{search_query}%')
        ).subquery()
        
        # Search in skills wanted
        skill_wanted_users = db.session.query(User.id).join(SkillWanted).filter(
            SkillWanted.name.ilike(f'%{search_query}%')
        ).subquery()
        
        query = query.filter(
            (User.id.in_(db.session.query(skill_users.c.id))) | 
            (User.id.in_(db.session.query(skill_wanted_users.c.id)))
        )
    
    if category:
        # Filter by category in skills offered or wanted
        skill_users = db.session.query(User.id).join(Skill).filter(
            Skill.category == category
        ).subquery()
        
        skill_wanted_users = db.session.query(User.id).join(SkillWanted).filter(
            SkillWanted.category == category
        ).subquery()
        
        query = query.filter(
            (User.id.in_(db.session.query(skill_users.c.id))) | 
            (User.id.in_(db.session.query(skill_wanted_users.c.id)))
        )
    
    users = query.all()
    
    return render_template('browse.html', users=users, search_form=search_form)

@app.route('/user/<int:user_id>')
@login_required
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    if not user.is_public and user.id != current_user.id:
        flash('This profile is private', 'error')
        return redirect(url_for('browse'))
    
    # Get potential swap options
    swap_form = SwapRequestForm()
    swap_form.skill_offered.choices = [(s.name, s.name) for s in current_user.skills_offered]
    swap_form.skill_wanted.choices = [(s.name, s.name) for s in user.skills_offered]
    
    return render_template('profile.html', user=user, swap_form=swap_form, viewing_other=True)

@app.route('/send_request/<int:user_id>', methods=['POST'])
@login_required
def send_request(user_id):
    user = User.query.get_or_404(user_id)
    skill_offered = request.form.get('skill_offered')
    skill_wanted = request.form.get('skill_wanted')
    message = request.form.get('message', '')
    
    # Check if request already exists
    existing_request = SwapRequest.query.filter_by(
        requester_id=current_user.id,
        requested_id=user_id,
        skill_offered=skill_offered,
        skill_wanted=skill_wanted,
        status='pending'
    ).first()
    
    if existing_request:
        flash('You already have a pending request for this skill swap', 'error')
    else:
        swap_request = SwapRequest(
            requester_id=current_user.id,
            requested_id=user_id,
            skill_offered=skill_offered,
            skill_wanted=skill_wanted,
            message=message
        )
        
        # Increment notification count for the requested user
        user.unread_notifications = (user.unread_notifications or 0) + 1
        
        db.session.add(swap_request)
        db.session.commit()
        flash('Swap request sent successfully', 'success')
    
    return redirect(url_for('view_user', user_id=user_id))

@app.route('/requests')
@login_required
def requests():
    received_requests = SwapRequest.query.filter_by(requested_id=current_user.id, status='pending').all()
    sent_requests = SwapRequest.query.filter_by(requester_id=current_user.id).all()
    
    # Mark notifications as read when viewing requests
    current_user.unread_notifications = 0
    db.session.commit()
    
    return render_template('dashboard.html', 
                         received_requests=received_requests,
                         sent_requests=sent_requests,
                         show_requests=True)

@app.route('/handle_request/<int:request_id>/<action>')
@login_required
def handle_request(request_id, action):
    swap_request = SwapRequest.query.get_or_404(request_id)
    
    if swap_request.requested_id != current_user.id:
        flash('Unauthorized action', 'error')
        return redirect(url_for('requests'))
    
    if action == 'accept':
        swap_request.status = 'accepted'
        flash('Request accepted', 'success')
        # Notify requester
        requester = User.query.get(swap_request.requester_id)
        requester.unread_notifications = (requester.unread_notifications or 0) + 1
    elif action == 'decline':
        swap_request.status = 'declined'
        flash('Request declined', 'info')
        # Notify requester
        requester = User.query.get(swap_request.requester_id)
        requester.unread_notifications = (requester.unread_notifications or 0) + 1
    
    swap_request.updated_at = datetime.utcnow()
    db.session.commit()
    
    return redirect(url_for('requests'))

@app.route('/cancel_request/<int:request_id>')
@login_required
def cancel_request(request_id):
    swap_request = SwapRequest.query.get_or_404(request_id)
    
    if swap_request.requester_id != current_user.id:
        flash('Unauthorized action', 'error')
        return redirect(url_for('requests'))
    
    if swap_request.status == 'pending':
        db.session.delete(swap_request)
        db.session.commit()
        flash('Request cancelled', 'info')
    
    return redirect(url_for('requests'))

@app.route('/complete_swap/<int:request_id>')
@login_required
def complete_swap(request_id):
    swap_request = SwapRequest.query.get_or_404(request_id)
    
    if swap_request.requester_id != current_user.id and swap_request.requested_id != current_user.id:
        flash('Unauthorized action', 'error')
        return redirect(url_for('requests'))
    
    swap_request.status = 'completed'
    swap_request.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Swap marked as completed', 'success')
    return redirect(url_for('feedback', request_id=request_id))

@app.route('/feedback/<int:request_id>', methods=['GET', 'POST'])
@login_required
def feedback(request_id):
    swap_request = SwapRequest.query.get_or_404(request_id)
    
    # Determine who to give feedback to
    if swap_request.requester_id == current_user.id:
        feedback_to = swap_request.requested
    elif swap_request.requested_id == current_user.id:
        feedback_to = swap_request.requester
    else:
        flash('Unauthorized action', 'error')
        return redirect(url_for('dashboard'))
    
    # Check if feedback already given
    existing_feedback = Feedback.query.filter_by(
        from_user_id=current_user.id,
        to_user_id=feedback_to.id,
        swap_request_id=request_id
    ).first()
    
    if existing_feedback:
        flash('You have already provided feedback for this swap', 'info')
        return redirect(url_for('dashboard'))
    
    form = FeedbackForm()
    
    if form.validate_on_submit():
        feedback_obj = Feedback(
            from_user_id=current_user.id,
            to_user_id=feedback_to.id,
            swap_request_id=request_id,
            rating=form.rating.data,
            comment=form.comment.data
        )
        db.session.add(feedback_obj)
        db.session.commit()
        flash('Feedback submitted successfully', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('feedback.html', form=form, swap_request=swap_request, feedback_to=feedback_to)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Get statistics
    total_users = User.query.count()
    total_swaps = SwapRequest.query.count()
    active_swaps = SwapRequest.query.filter_by(status='accepted').count()
    pending_requests = SwapRequest.query.filter_by(status='pending').count()
    completed_swaps = SwapRequest.query.filter_by(status='completed').count()
    
    # Get recent activity
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    recent_swaps = SwapRequest.query.order_by(SwapRequest.created_at.desc()).limit(10).all()
    recent_feedback = Feedback.query.order_by(Feedback.created_at.desc()).limit(10).all()
    
    return render_template('admin_dashboard.html',
                         total_users=total_users,
                         total_skills=total_swaps,
                         pending_requests=pending_requests,
                         completed_swaps=completed_swaps,
                         recent_users=recent_users,
                         recent_requests=recent_swaps)

@app.route('/admin/ban_user/<int:user_id>')
@login_required
def ban_user(user_id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash('Cannot ban admin user', 'error')
    else:
        # Cancel all pending requests
        SwapRequest.query.filter(
            (SwapRequest.requester_id == user_id) | (SwapRequest.requested_id == user_id)
        ).filter_by(status='pending').update({'status': 'cancelled'})
        
        # Set profile to private
        user.is_public = False
        db.session.commit()
        flash(f'User {user.full_name} has been banned', 'success')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/unban_user/<int:user_id>')
@login_required
def unban_user(user_id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash('Cannot unban admin user', 'error')
    else:
        # Set profile to public (unban the user)
        user.is_public = True
        db.session.commit()
        flash(f'User {user.full_name} has been unbanned', 'success')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/message', methods=['GET', 'POST'])
@login_required
def admin_message():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    form = AdminMessageForm()
    
    if form.validate_on_submit():
        message = AdminMessage(
            title=form.title.data,
            content=form.content.data,
            created_by=current_user.id
        )
        db.session.add(message)
        db.session.commit()
        flash('Platform message sent successfully', 'success')
        return redirect(url_for('admin'))
    
    return render_template('admin.html', message_form=form, show_message_form=True)

@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.filter_by(is_admin=False).order_by(User.created_at.desc()).all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/requests')
@login_required
def admin_requests():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    requests = SwapRequest.query.order_by(SwapRequest.created_at.desc()).all()
    return render_template('admin_requests.html', requests=requests)

@app.route('/messages')
@login_required
def messages():
    admin_messages = AdminMessage.query.order_by(AdminMessage.created_at.desc()).all()
    return render_template('dashboard.html', admin_messages=admin_messages, show_messages=True)

@app.route('/api/completed-swaps')
@login_required
def api_completed_swaps():
    completed_swaps = SwapRequest.query.filter(
        ((SwapRequest.requester_id == current_user.id) | (SwapRequest.requested_id == current_user.id)) &
        (SwapRequest.status == 'completed')
    ).order_by(SwapRequest.updated_at.desc()).all()
    
    swaps_data = []
    for swap in completed_swaps:
        # Determine the other user
        other_user = swap.requested if swap.requester_id == current_user.id else swap.requester
        
        # Get feedback for this swap
        feedback = Feedback.query.filter_by(
            swap_request_id=swap.id,
            to_user_id=current_user.id
        ).first()
        
        swap_data = {
            'id': swap.id,
            'skill_offered': swap.skill_offered,
            'skill_wanted': swap.skill_wanted,
            'completed_at': swap.updated_at.isoformat(),
            'other_user': {
                'id': other_user.id,
                'full_name': other_user.full_name,
                'profile_photo': other_user.profile_photo
            },
            'feedback': {
                'rating': feedback.rating,
                'comment': feedback.comment
            } if feedback else None
        }
        swaps_data.append(swap_data)
    
    return jsonify({'swaps': swaps_data})

@app.route('/api/notifications')
@login_required
def api_notifications():
    return jsonify({'unread_count': current_user.unread_notifications or 0})

@app.route('/api/active-swaps')
@login_required
def api_active_swaps():
    active_swaps = SwapRequest.query.filter(
        ((SwapRequest.requester_id == current_user.id) | (SwapRequest.requested_id == current_user.id)) &
        (SwapRequest.status == 'accepted')
    ).order_by(SwapRequest.updated_at.desc()).all()
    
    swaps_data = []
    for swap in active_swaps:
        # Determine the other user
        other_user = swap.requested if swap.requester_id == current_user.id else swap.requester
        
        swap_data = {
            'id': swap.id,
            'skill_offered': swap.skill_offered,
            'skill_wanted': swap.skill_wanted,
            'accepted_at': swap.updated_at.isoformat(),
            'other_user': {
                'id': other_user.id,
                'full_name': other_user.full_name,
                'profile_photo': other_user.profile_photo,
                'availability': other_user.availability
            },
            'message': swap.message
        }
        swaps_data.append(swap_data)
    
    return jsonify({'swaps': swaps_data})

@app.route('/api/pending-requests')
@login_required
def api_pending_requests():
    pending_requests = SwapRequest.query.filter(
        ((SwapRequest.requester_id == current_user.id) | (SwapRequest.requested_id == current_user.id)) &
        (SwapRequest.status == 'pending')
    ).order_by(SwapRequest.created_at.desc()).all()
    
    requests_data = []
    for request in pending_requests:
        # Determine if this is sent or received
        is_sent = request.requester_id == current_user.id
        other_user = request.requested if is_sent else request.requester
        
        request_data = {
            'id': request.id,
            'skill_offered': request.skill_offered,
            'skill_wanted': request.skill_wanted,
            'created_at': request.created_at.isoformat(),
            'is_sent': is_sent,
            'other_user': {
                'id': other_user.id,
                'full_name': other_user.full_name,
                'profile_photo': other_user.profile_photo
            },
            'message': request.message
        }
        requests_data.append(request_data)
    
    return jsonify({'requests': requests_data})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('base.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base.html', error='Internal server error'), 500