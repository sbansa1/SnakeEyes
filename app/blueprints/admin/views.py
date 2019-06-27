from flask import render_template, request, flash, url_for
from flask_login import current_user
from werkzeug.utils import redirect

from app.blueprints.admin import admin_blu
from app.blueprints.admin.forms import SearchForm, BulkDeleteAll, UserForm
from app.blueprints.admin.model import DashBoard
from app.blueprints.user.model import User


@admin_blu.before_request
def before_request():
    """Protect all of the Admin end points"""
    pass

# Dashboard -------------------------------------------------------------------
@admin_blu.route('/')
def dashboard():
    result = DashBoard.group_count_method()
    return render_template( 'admin/page/dashboard.html',
                            group_and_count_users=result)


# User -------------------------------------------------------------------------

@admin_blu.route("/users",defaults={"page":1})
@admin_blu.route(("/users/page/<int:page>"))
def users(page):
    search_form = SearchForm()
    bulk_form = BulkDeleteAll()

    sort_by = ( request.args.get( 'sort', 'created_on' ),
                            request.args.get( 'direction', 'desc' ))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_users = User.query \
        .filter( User.search(request.args.get( 'q', 'sort'))) \
        .order_by( User.role.asc())\
        .paginate( page, 50, True )

    return render_template( 'admin/user/index.html',
                            form=search_form, bulk_form=bulk_form,
                            users=paginated_users)


@admin_blu.route('/users/edit/<int:id>', methods=['GET', 'POST'])
def users_edit(id):
    user = User.query.get(id)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        if User.is_last_admin(user,
                              request.form.get('role'),
                              request.form.get('active')):
            flash('You are the last admin, you cannot do that.', 'error')
            return redirect(url_for('admin.users'))

        form.populate_obj(user)

        if not user.username:
            user.username = None

        user.save()

        flash('User has been saved successfully.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/user/edit.html', form=form, user=user)


@admin_blu.route('/users/bulk_delete', methods=['POST'])
def users_bulk_delete():
    form = BulkDeleteAll()

    if form.validate_on_submit():
        ids = User.get_bulk_action_ids(request.form.get('scope'),
                                       request.form.getlist('bulk_ids'),
                                       omit_ids=[current_user.id],
                                       query=request.args.get('q', ''))

        delete_count = User.bulk_delete(ids)

        flash('{0} user(s) were scheduled to be deleted.'.format(delete_count),
              'success')
    else:
        flash('No users were deleted, something went wrong.', 'error')

    return redirect(url_for('admin.users'))

