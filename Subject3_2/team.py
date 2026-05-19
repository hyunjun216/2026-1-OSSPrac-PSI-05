import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'oss-team-secret-key-2026'

UPLOAD_FOLDER = os.path.join(app.static_folder, 'img')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 기본 팀원 데이터 (로컬 이미지 사용)
DEFAULT_MEMBERS = [
    {
        "id": 1,
        "name": "김양우",
        "student_id": "20245678",
        "gender": "남성",
        "department": "컴퓨터공학과",
        "languages": ["python", "cplusplus", "java", "matlab"],
        "role": "백엔드 개발 및 서버 아키텍처 설계",
        "intro": "시스템 프로그래밍과 로우레벨 아키텍처에 관심이 많은 개발자입니다. 전체적인 시스템 구조 설계와 안정적인 서버 구축을 담당하고 있습니다.",
        "contribution": "Flask 기반의 REST API 설계 및 구현, 데이터베이스 모델링, 로깅 및 예외 처리 시스템 구축",
        "photo": "/static/img/member1.png",
        "github": "https://github.com/kimyangwoo",
        "email": "yangwoo@example.com",
        "portfolio": "https://yangwoo.dev"
    },
    {
        "id": 2,
        "name": "박현준",
        "student_id": "20245678",
        "gender": "남성",
        "department": "소프트웨어학과",
        "languages": ["javascript", "html5", "react"],
        "role": "프론트엔드 개발 및 UI/UX",
        "intro": "직관적이고 사용자 친화적인 웹 인터페이스를 고민하는 개발자입니다. 프로젝트의 얼굴이 되는 웹 페이지의 디자인과 클라이언트 로직을 책임집니다.",
        "contribution": "Bootstrap을 활용한 반응형 UI/UX 디자인, 다크모드 및 애니메이션 구현, 컴포넌트 기반 아키텍처 설계",
        "photo": "/static/img/member2.png",
        "github": "https://github.com/parkhyunjun",
        "email": "hyunjun@example.com",
        "portfolio": "https://hyunjun.design"
    },
    {
        "id": 3,
        "name": "임여민",
        "student_id": "20249012",
        "gender": "여성",
        "department": "인공지능학과",
        "languages": ["python", "sqldeveloper", "r"],
        "role": "데이터베이스 설계 및 데이터 처리",
        "intro": "데이터의 흐름을 분석하고 구조화하는 것을 좋아합니다. 프로젝트 내 DB 스키마 설계 및 효율적인 데이터 파이프라인 구축을 맡고 있습니다.",
        "contribution": "RDB 스키마 정규화 및 최적화, 대용량 데이터 처리 파이프라인 설계, 데이터 시각화 컴포넌트 연동",
        "photo": "/static/img/member3.png",
        "github": "https://github.com/Yeomin-Yim",
        "email": "yeomin@example.com",
        "portfolio": "https://yeomin.data"
    },
    {
        "id": 4,
        "name": "김준성",
        "student_id": "20243456",
        "gender": "남성",
        "department": "컴퓨터공학과",
        "languages": ["c", "bash", "docker"],
        "role": "인프라 구축 및 배포 관리",
        "intro": "안정적인 서비스 운영과 자동화에 관심이 많습니다. 완성된 프로젝트가 Nginx와 연동되어 원활하게 배포될 수 있도록 서버 환경을 구성합니다.",
        "contribution": "Docker 기반의 컨테이너화, Nginx 리버스 프록시 설정, CI/CD 파이프라인 구축 및 무중단 배포 적용",
        "photo": "/static/img/member4.png",
        "github": "https://github.com/kimjunsung",
        "email": "junsung@example.com",
        "portfolio": "https://junsung.infra"
    }
]

def get_members():
    if 'members' not in session:
        session['members'] = DEFAULT_MEMBERS
    return session['members']

def save_members(members):
    session['members'] = members

def next_id(members):
    return max((m['id'] for m in members), default=0) + 1

@app.route('/')
def index():
    members = get_members()
    return render_template('index.html', members=members)

@app.route('/member/<int:member_id>')
def member_detail(member_id):
    members = get_members()
    member = next((m for m in members if m['id'] == member_id), None)
    if member:
        return render_template('member.html', member=member)
    return render_template('404.html'), 404

@app.route('/input')
def input_page():
    return render_template('input.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/result', methods=['POST'])
def result_page():
    name = request.form.get('name', '').strip()
    student_id = request.form.get('student_id', '').strip()
    gender = request.form.get('gender', '').strip()
    department = request.form.get('department', '').strip()
    languages = request.form.getlist('languages')

    # 서버측 검증
    errors = []
    if not name:
        errors.append('이름을 입력해주세요.')
    if not student_id:
        errors.append('학번을 입력해주세요.')
    if not gender:
        errors.append('성별을 선택해주세요.')
    if not department:
        errors.append('학과를 입력해주세요.')
    if not languages:
        errors.append('프로그래밍 언어를 최소 1개 선택해주세요.')

    if errors:
        for e in errors:
            flash(e, 'danger')
        return redirect(url_for('input_page'))

    # 사진 업로드 처리
    photo_path = '/static/img/default.svg'
    photo = request.files.get('photo')
    if photo and photo.filename:
        from werkzeug.utils import secure_filename
        filename = secure_filename(f"{student_id}_{photo.filename}")
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        photo_path = f'/static/img/{filename}'

    members = get_members()
    new_member = {
        "id": next_id(members),
        "name": name,
        "student_id": student_id,
        "gender": gender,
        "department": department,
        "languages": languages,
        "role": request.form.get('role', '').strip() or "Team Member",
        "intro": request.form.get('intro', '').strip() or f"{department} 소속 팀원입니다.",
        "contribution": request.form.get('contribution', '').strip() or "",
        "photo": photo_path,
        "github": request.form.get('github', '').strip() or "#",
        "email": request.form.get('email', '').strip() or "",
        "portfolio": request.form.get('portfolio', '').strip() or "#"
    }
    members.append(new_member)
    save_members(members)
    flash(f'{name} 님이 팀에 추가되었습니다!', 'success')
    return render_template('result.html', member=new_member)

@app.route('/member/<int:member_id>/edit', methods=['GET', 'POST'])
def edit_member(member_id):
    members = get_members()
    member = next((m for m in members if m['id'] == member_id), None)
    if not member:
        return render_template('404.html'), 404

    if request.method == 'POST':
        member['name'] = request.form.get('name', '').strip() or member['name']
        member['student_id'] = request.form.get('student_id', '').strip() or member['student_id']
        member['gender'] = request.form.get('gender', '').strip() or member['gender']
        member['department'] = request.form.get('department', '').strip() or member['department']
        member['role'] = request.form.get('role', '').strip() or member['role']
        member['intro'] = request.form.get('intro', '').strip() or member['intro']
        member['contribution'] = request.form.get('contribution', '').strip() or member['contribution']
        member['github'] = request.form.get('github', '').strip() or member['github']
        member['email'] = request.form.get('email', '').strip() or member['email']
        member['portfolio'] = request.form.get('portfolio', '').strip() or member['portfolio']
        langs = request.form.getlist('languages')
        if langs:
            member['languages'] = langs

        photo = request.files.get('photo')
        if photo and photo.filename:
            from werkzeug.utils import secure_filename
            filename = secure_filename(f"{member['student_id']}_{photo.filename}")
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            member['photo'] = f'/static/img/{filename}'

        save_members(members)
        flash(f'{member["name"]} 님의 정보가 수정되었습니다.', 'success')
        return redirect(url_for('member_detail', member_id=member_id))

    return render_template('edit.html', member=member)

@app.route('/member/<int:member_id>/delete', methods=['POST'])
def delete_member(member_id):
    members = get_members()
    member = next((m for m in members if m['id'] == member_id), None)
    if member:
        members = [m for m in members if m['id'] != member_id]
        save_members(members)
        flash(f'{member["name"]} 님이 팀에서 제거되었습니다.', 'warning')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

import json
import os

MESSAGES_FILE = 'messages.json'

def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_message(msg):
    messages = load_messages()
    messages.append(msg)
    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        msg = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'message': request.form.get('message')
        }
        save_message(msg)
        return redirect('/messages')
    all_messages = load_messages()
    return render_template('messages.html', messages=all_messages)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
