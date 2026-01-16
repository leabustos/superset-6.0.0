#!/usr/bin/env python3
import logging
import sys
import os
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_database(app, max_retries=30):
    """Wait for database connection to be ready"""
    with app.app_context():
        from superset.extensions import db
        from sqlalchemy.exc import OperationalError
        
        for attempt in range(max_retries):
            try:
                # Try to execute a simple query
                db.session.execute("SELECT 1")
                logger.info("Database connection successful")
                return True
            except OperationalError as e:
                logger.warning(f"Database not ready (attempt {attempt + 1}/{max_retries}): {e}")
                time.sleep(2)
        
        logger.error("Database connection failed after max retries")
        return False

def create_public_role():
    """Create or update the Public role with permissions"""
    # Set environment variables
  
    # Import here after setting env vars
    from superset.app import create_app
    from superset.extensions import db
    from flask_appbuilder.security.sqla.models import Role
    
    # Create the Flask application
    app = create_app()
    
    # Wait for database
    if not wait_for_database(app):
        sys.exit(1)
    
    with app.app_context():
        try:
            # Create or get Public role
            public_role = db.session.query(Role).filter_by(name="Public").first()
            
            if not public_role:
                public_role = Role(name="Public")
                db.session.add(public_role)
                db.session.commit()
                logger.info("Created Public role")
            else:
                logger.info("Public role already exists")
            
            # Note: We're not adding permissions here because:
            # 1. Permissions might be added via the UI
            # 2. The Gamma role might not exist yet
            # 3. You can use PUBLIC_ROLE_LIKE_GAMMA in config.py
            
            logger.info("✅ Public role setup completed")
            
        except Exception as e:
            logger.error(f"Error: {e}")
            db.session.rollback()
            sys.exit(1)

if __name__ == "__main__":
    create_public_role()

# #!/usr/bin/env python3
# import logging
# from superset import app, db
# from flask_appbuilder.security.sqla.models import Role, Permission, PermissionView
# from flask_appbuilder.security.sqla.models import ViewMenu
# from flask_appbuilder.security.sqla.models import assoc_permissionview_role

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def create_public_role():
#     with app.app_context():
#         # Create or get Public role
#         public_role = db.session.query(Role).filter_by(name="Public").first()
        
#         if not public_role:
#             public_role = Role(name="Public")
#             db.session.add(public_role)
#             logger.info("Created Public role")
#         else:
#             logger.info("Public role already exists")
        
#         # Get Gamma role to copy permissions from
#         gamma_role = db.session.query(Role).filter_by(name="Gamma").first()
        
#         if gamma_role:
#             # Copy permissions from Gamma to Public
#             for permission_view in gamma_role.permissions:
#                 if permission_view not in public_role.permissions:
#                     public_role.permissions.append(permission_view)
#             logger.info("Copied Gamma permissions to Public role")
        
#         # Add specific permissions for public access
#         # Get necessary permissions
#         view_menu_names = [
#             "Dashboard", 
#             "DashboardModelView", 
#             "can_list", 
#             "can_show",
#             "ResetPasswordView", 
#             "RoleModelView"
#         ]
        
#         for view_menu_name in view_menu_names:
#             view_menu = db.session.query(ViewMenu).filter_by(name=view_menu_name).first()
#             if view_menu:
#                 # Get can_read permission
#                 perm_view = db.session.query(PermissionView).filter_by(
#                     permission=db.session.query(Permission).filter_by(name="can_read").first(),
#                     view_menu=view_menu
#                 ).first()
                
#                 if perm_view and perm_view not in public_role.permissions:
#                     public_role.permissions.append(perm_view)
        
#         db.session.commit()
#         logger.info("Public role configured successfully")

# if __name__ == "__main__":
#     create_public_role()