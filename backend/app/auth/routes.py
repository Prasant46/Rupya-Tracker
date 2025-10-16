from flask import Blueprint, request, jsonify, current_app, redirect, make_response
from app.extensions import db, jwt
from app.models.user import User
from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies


bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["POST"])
def register():
  
  data = request.get_json() or {}
  if not data :
    return jsonify({
              "success": False,
              "message": "Data should not be empty"
            }), 400   
    
  name = data.get("name")
  email = data.get("email")
  password = data.get("password")
  
  if not (name and email and password):
    return jsonify({
      "success":False,
      "message":"Enter Valid Credentials"
    }), 400
  
  if User.query.filter_by(email=email).first():
    return jsonify({
      "success":False,
      "message":"User with this email already exists"
    }), 400
  
  user = User(name=name, email=email)
  user.password_hash = bcrypt.hash(password)
  db.session.add(user)
  db.session.commit()
  
  # Create access token
  access_token = create_access_token(identity=user.account_id)
  
  # Create response with cookie
  response = make_response(jsonify({
    "success": True,
    "message": "User registered successfully",
    "data": user.to_dict()
  }), 201)
  
  # Set HTTP-only cookie with token
  response.set_cookie(
    'access_token_cookie',
    value=access_token,
    httponly=True,
    secure=current_app.config.get('FLASK_ENV') == 'production',  # True in production (HTTPS only)
    samesite='Lax',
    max_age=3600 * 24 * 7  # 7 days
  )
  
  return response
  
  
@bp.route("/login", methods=["POST"])
def login():
  data = request.get_json() or {}
  if not data :
    return jsonify({
              "success": False,
              "message": "Data should not be empty"
            }), 400   
    
  email = data.get("email")
  password = data.get("password")
  
  if not (email and password):
    return jsonify({
      "success":False,
      "message":"Enter Valid Credentials"
    }), 400
  
  user = User.query.filter_by(email=email).first()
  if not user or not user.password_hash or not bcrypt.verify(password, user.password_hash):
    return jsonify({
      "success":False,
      "message":"Invalid email or password"
    }), 401
  
  # Create access token
  access_token = create_access_token(identity=user.account_id)
  
  # Create response with cookie
  response = make_response(jsonify({
    "success": True,
    "message": "Login successful",
    "data": user.to_dict()
  }), 200)
  
  # Set HTTP-only cookie with token
  response.set_cookie(
    'access_token_cookie',
    value=access_token,
    httponly=True,
    secure=current_app.config.get('FLASK_ENV') == 'production',  # True in production
    samesite='Lax',
    max_age=3600 * 24 * 7  # 7 days
  )
  
  return response
  
@bp.route("/logout", methods=["POST"])
def logout():
  response = make_response(jsonify({
    "success": True,
    "message": "Logout successful"
  }), 200)
  
  # Clear the cookie
  unset_jwt_cookies(response)
  
  return response
  
@bp.route("/me", methods=["GET"])
@jwt_required(optional=True)
def me():
  identity = get_jwt_identity()
  if not identity:
    return jsonify({
      "success": True,
      "message": "No user logged in",
      "data": None
    }), 200
  user = User.query.filter_by(account_id=identity).first()
  if not user:
    return jsonify({
      "success": True,
      "message": "User not found",
      "data": None
    }), 200
  return jsonify({
    "success": True,
    "message": "User profile fetched successfully",
    "data": user.to_dict()
  }), 200
  
@bp.route("/oauth/github", methods=["GET"])
def github_oauth():
  github_client_id = current_app.config.get("GITHUB_CLIENT_ID")
  # Backend callback URL - GitHub will redirect here after user authorization
  redirect_uri = request.host_url.rstrip('/') + "/auth/oauth/github/callback"
  
  return redirect(f"https://github.com/login/oauth/authorize?client_id={github_client_id}&redirect_uri={redirect_uri}&scope=user:email")

@bp.route("/oauth/github/callback", methods=["GET"])
def github_oauth_callback():
  import requests
  import uuid
  
  # Get authorization code from query params
  code = request.args.get('code')
  if not code:
    frontend_url = current_app.config.get("FRONTEND_URL")
    return redirect(f"{frontend_url}/sign-in?authstatus=failed")
  
  try:
    # Exchange code for access token
    token_url = "https://github.com/login/oauth/access_token"
    token_data = {
      "client_id": current_app.config.get("GITHUB_CLIENT_ID"),
      "client_secret": current_app.config.get("GITHUB_CLIENT_SECRET"),
      "code": code
    }
    token_headers = {"Accept": "application/json"}
    
    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    token_json = token_response.json()
    
    access_token = token_json.get("access_token")
    if not access_token:
      frontend_url = current_app.config.get("FRONTEND_URL")
      return redirect(f"{frontend_url}/sign-in?authstatus=failed")
    
    # Get user info from GitHub
    user_url = "https://api.github.com/user"
    user_headers = {"Authorization": f"Bearer {access_token}"}
    user_response = requests.get(user_url, headers=user_headers)
    user_data = user_response.json()
    
    # Get user email (might be in a separate endpoint)
    email = user_data.get("email")
    if not email:
      email_url = "https://api.github.com/user/emails"
      email_response = requests.get(email_url, headers=user_headers)
      emails = email_response.json()
      # Get primary verified email
      for e in emails:
        if e.get("primary") and e.get("verified"):
          email = e.get("email")
          break
      if not email and emails:
        email = emails[0].get("email")
    
    if not email:
      frontend_url = current_app.config.get("FRONTEND_URL")
      return redirect(f"{frontend_url}/sign-in?authstatus=failed")
    
    # Check if user exists
    user = User.query.filter_by(email=email).first()
    
    if not user:
      # Create new user
      user = User(
        name=user_data.get("name") or user_data.get("login"),
        email=email,
        avatar_url=user_data.get("avatar_url")
      )
      # OAuth users don't have password
      user.password_hash = None
      db.session.add(user)
      db.session.commit()
    
    # Create JWT token
    jwt_token = create_access_token(identity=user.account_id)
    
    # Redirect to frontend with token
    frontend_url = current_app.config.get("FRONTEND_URL")
    response = make_response(redirect(f"{frontend_url}/sign-in?authstatus=success&token={jwt_token}"))
    
    return response
    
  except Exception as e:
    print(f"GitHub OAuth error: {str(e)}")
    frontend_url = current_app.config.get("FRONTEND_URL")
    return redirect(f"{frontend_url}/sign-in?authstatus=failed")

@bp.route("/oauth/google", methods=["GET"])
def google_oauth():
  google_client_id = current_app.config.get("GOOGLE_CLIENT_ID")
  # Backend callback URL - Google will redirect here after user authorization
  redirect_uri = request.host_url.rstrip('/') + "/auth/oauth/google/callback"
  
  scope = "openid email profile"
  return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={google_client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}")

@bp.route("/oauth/google/callback", methods=["GET"])
def google_oauth_callback():
  import requests
  import uuid
  
  # Get authorization code from query params
  code = request.args.get('code')
  if not code:
    frontend_url = current_app.config.get("FRONTEND_URL")
    return redirect(f"{frontend_url}/sign-in?authstatus=failed")
  
  try:
    # Exchange code for access token
    token_url = "https://oauth2.googleapis.com/token"
    redirect_uri = request.host_url.rstrip('/') + "/auth/oauth/google/callback"
    token_data = {
      "client_id": current_app.config.get("GOOGLE_CLIENT_ID"),
      "client_secret": current_app.config.get("GOOGLE_CLIENT_SECRET"),
      "code": code,
      "grant_type": "authorization_code",
      "redirect_uri": redirect_uri
    }
    
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()
    
    access_token = token_json.get("access_token")
    if not access_token:
      frontend_url = current_app.config.get("FRONTEND_URL")
      return redirect(f"{frontend_url}/sign-in?authstatus=failed")
    
    # Get user info from Google
    user_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    user_headers = {"Authorization": f"Bearer {access_token}"}
    user_response = requests.get(user_url, headers=user_headers)
    user_data = user_response.json()
    
    email = user_data.get("email")
    if not email:
      frontend_url = current_app.config.get("FRONTEND_URL")
      return redirect(f"{frontend_url}/sign-in?authstatus=failed")
    
    # Check if user exists
    user = User.query.filter_by(email=email).first()
    
    if not user:
      # Create new user
      user = User(
        name=user_data.get("name"),
        email=email,
        avatar_url=user_data.get("picture")
      )
      # OAuth users don't have password
      user.password_hash = None
      db.session.add(user)
      db.session.commit()
    
    # Create JWT token
    jwt_token = create_access_token(identity=user.account_id)
    
    # Redirect to frontend with token
    frontend_url = current_app.config.get("FRONTEND_URL")
    response = make_response(redirect(f"{frontend_url}/sign-in?authstatus=success&token={jwt_token}"))
    
    return response
    
  except Exception as e:
    print(f"Google OAuth error: {str(e)}")
    frontend_url = current_app.config.get("FRONTEND_URL")
    return redirect(f"{frontend_url}/sign-in?authstatus=failed")

    
  
  
    
  
  