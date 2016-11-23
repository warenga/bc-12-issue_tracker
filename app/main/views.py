from flask import session, render_template, redirect, url_for, request, flash
from . import main
from .. import db
from ..models import Issues
from .forms import IssueForm, MarkIssueForm
from flask.ext.login import current_user, login_required
from .decorators import required_roles

@main.route('/home', methods=['GET', 'POST'])
@login_required
def homepage():
	if current_user.role.id == 1:
		issues = Issues.query.filter_by(department=current_user.department).all()
	else:
		issues = Issues.query.all()
	return render_template('home.html', issues=issues)

@main.route('/new_issue', methods=['GET', 'POST'])
def new_issue():
	issue_form = IssueForm()
	if issue_form.validate_on_submit():
		issue = Issues(title=issue_form.title.data,
						description=issue_form.description.data,
						department=issue_form.department.data,
						priority=issue_form.priority.data,
						raised_by = current_user._get_current_object()
						)
		db.session.add(issue)
		db.session.commit()
		flash('You issue has been raised. You shall get feedback soon')
		return redirect(url_for('.homepage'))
	return render_template('new_issue.html', issue_form=issue_form)


@main.route('/admin_view/<int:id>', methods=['GET','POST'])
def check_issues(id):
	issue = Issues.query.get_or_404(id)
	check_form = MarkIssueForm()
	if request.method == 'POST' and check_form.validate():
		issue.assigned_to = check_form.assigned_to.data
		issue.progress = check_form.progress.data
		db.session.add(issue)
		db.session.commit()
		return redirect(url_for('.homepage'))
	return render_template('check_issue.html', issues=[issue], check_form=check_form) 
