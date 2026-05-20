# 🌐 Subject3_2 — 팀 포트폴리오 웹사이트

> 팀 PSI-05의 포트폴리오 웹사이트입니다. 팀원 소개 및 프로필 관리, 방문자 메시지 기능을 제공합니다.
> 팀원 소개는 [상위 README](../README.md)를 참고해주세요.

---

## 📌 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 프로젝트명 | OSS Project Team 포트폴리오 웹사이트 |
| 기술 스택 | Flask (Python) + Jinja2 + Bootstrap 5 |
| 실행 포트 | 5000 |

---

## 🛠 기술 스택

- **Backend**: Python 3, Flask, Jinja2
- **Frontend**: Bootstrap 5.3, FontAwesome 6.4, Devicon 2.15
- **폰트**: Pretendard (한글 웹폰트)
- **데이터 저장**: Flask Session (팀원 데이터), JSON 파일 (방문자 메시지)

---

## 🚀 설치 및 실행 방법

```bash
# 1. 해당 폴더로 이동
cd Subject3_2

# 2. 의존성 설치
pip install flask werkzeug

# 3. 서버 실행
python team.py
```

브라우저에서 `http://localhost:5000` 접속

---

## 📁 폴더 구조

```
Subject3_2/
├── team.py                 # Flask 메인 서버
├── messages.json           # 방문자 메시지 저장 파일
├── static/
│   └── img/                # 팀원 프로필 사진 저장 폴더
└── templates/
    ├── base.html           # 공통 레이아웃 (네비게이션, 다크모드 등)
    ├── index.html          # 메인 페이지 (팀 소개)
    ├── member.html         # 멤버 상세 프로필
    ├── input.html          # 멤버 등록 폼
    ├── result.html         # 멤버 등록 결과
    ├── edit.html           # 멤버 정보 수정 폼
    ├── contact.html        # 연락처 페이지
    ├── messages.html       # 방문자 메시지 페이지
    └── 404.html            # 커스텀 에러 페이지
```

---

## ⚙️ 주요 기능

### 1. 팀원 CRUD 관리

| 기능 | 경로 | 메서드 | 설명 |
|------|------|--------|------|
| 팀원 목록 조회 | `/` | GET | 전체 팀원을 메인 페이지에 표시 |
| 팀원 상세 조회 | `/member/<id>` | GET | 개별 프로필 페이지 |
| 팀원 추가 | `/result` | POST | 폼 입력 + 사진 업로드로 새 멤버 등록 |
| 팀원 수정 | `/member/<id>/edit` | GET/POST | 기존 멤버 정보 수정 + 사진 교체 |
| 팀원 삭제 | `/member/<id>/delete` | POST | 팀원 제거 |

### 2. 방문자 메시지

| 기능 | 경로 | 메서드 | 설명 |
|------|------|--------|------|
| 메시지 조회/등록 | `/messages` | GET/POST | 방문자 메시지 폼 표시 및 저장 |
| 메시지 삭제 | `/messages/<index>/delete` | POST | 인덱스 기반으로 특정 메시지 삭제 |

- 방문자가 이름, 이메일, 메시지를 입력하면 `messages.json`에 저장됩니다.
- 저장된 메시지는 목록으로 확인하고 삭제할 수 있습니다.

### 3. 기타 백엔드 기능

- **서버측 유효성 검증**: 이름, 학번, 성별, 학과, 프로그래밍 언어 필수 입력 검증
- **사진 업로드**: `static/img/` 폴더에 저장, `secure_filename` 적용으로 보안 처리
- **세션 기반 저장**: Flask Session을 이용한 팀원 데이터 CRUD 상태 유지
- **Flash 메시지**: 추가/수정/삭제 시 Toast 형태 알림 표시
- **404 에러 처리**: 커스텀 404 에러 페이지 제공

---

## 🎨 UI/UX 기능

### 전역 기능 (base.html)

- **다크모드/라이트모드**: 기본값 다크모드, 네비게이션 토글로 전환, `localStorage`에 저장하여 재방문 시 유지
- **3D 블롭 배경 애니메이션**: blur 효과가 적용된 블롭 5개가 화면에 떠다니며 페이지 로드 시 0.2초 간격으로 순차 등장
- **네비게이션 바**: Glassmorphism 디자인(`backdrop-filter: blur(12px)`), 상단 고정, 스크롤 시 자동 축소, 현재 페이지 활성 표시
- **스크롤 프로그레스 바**: 페이지 상단에 오렌지 그라데이션 진행률 표시
- **스크롤 투 탑 버튼**: 300px 이상 스크롤 시 우하단에 등장
- **마우스 글로우**: 마우스 커서를 따라다니는 오렌지 원형 빛 효과
- **Flash Toast 알림**: Bootstrap toast로 자동 소멸되는 알림 메시지

### 메인 페이지 (index.html)

- **히어로 섹션**: 100vh 풀스크린, 배지 → 제목 → 설명 → 버튼 순 페이드인 인트로, `Innovative Team` / `Creative Developers` / `Open Source Builders` / `Future Engineers` 타이핑 애니메이션
- **Service Architecture 섹션**: Client → Nginx → WSGI → Flask → Database 5단계 흐름도, 주황색 점이 이동하는 애니메이션 커넥터, 노드 호버 시 강조 효과
- **멤버 쇼케이스 섹션**: 1인 1화면(90vh), 홀수 멤버는 사진 왼쪽/정보 오른쪽, 짝수 멤버는 반대 배치, 스크롤 시 정보 카드 슬라이드인 애니메이션, Glassmorphism 정보 카드

### 반응형 디자인

768px 이하 모바일 환경 대응: Architecture 흐름도 축소, 멤버 쇼케이스 세로 배치 전환, Tech Stack pill 중앙 정렬

---

## 🎨 디자인 시스템

| 항목 | 값 |
|------|----|
| 메인 컬러 | `#E8651A` (오렌지) |
| 라이트 오렌지 | `#FF8C42` |
| 다크 오렌지 | `#C44D0A` |
| 다크모드 배경 | `#0f0f0f` |
| 라이트모드 배경 | `#FFF3EA` |
| 폰트 | Pretendard |
| CSS 프레임워크 | Bootstrap 5.3 |
| 아이콘 | FontAwesome 6.4 + Devicon 2.15 |