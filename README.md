# DEV UNIVERSE

**universe**의 기술 블로그 · https://dev-universe.tech

Astro + Markdown 정적 사이트. 글 검색, 주제 필터, 라이트/다크 모드, 글 목차, RSS, sitemap을 제공합니다. 로그인·댓글·관리자 편집기는 포함하지 않습니다.

## 개발

Node.js 22.12 이상이 필요합니다.

```sh
npm ci
npm run dev
npm run build
```

## 글 쓰기

`src/content/posts/`에 Markdown 파일을 추가합니다. 파일 이름이 URL이 됩니다.

```yaml
---
title: "글 제목"
description: "한두 문장의 소개"
date: 2026-10-13
summary: "핵심 질문에 대한 답을 두세 문장으로 설명합니다."
# updated: 2026-10-14 # 본문을 실질적으로 수정한 날짜만 입력
category: "웹 개발"
tags: ["JavaScript", "실험"]
draft: true
---
```

본문은 일반 Markdown입니다. 공개하려면 `draft: false`로 바꿉니다. `public/images/`에 이미지를 추가하면 `/images/파일명`으로 사용할 수 있습니다. 코드와 콘텐츠에 키, 토큰, 내부 주소를 넣지 마세요. 검색 인덱스에는 공개 글 본문이 포함됩니다.

## GitHub와 배포

GitHub 연동은 코드·글의 버전 관리용입니다. **push만으로 운영 배포되지는 않습니다.** 현재 GitHub 인증에는 workflow 쓰기 권한이 없어 CI는 활성화하지 않았으며, 빌드 workflow 예제를 `docs/build-workflow.example.yml`에 제공합니다. 운영 서버 인증정보는 공개 저장소나 GitHub에 저장하지 않습니다.

관리자의 SSH 환경에서 다음 명령으로 배포합니다.

```sh
BLOG_SSH_HOST=hostinger ./scripts/deploy.sh
```

전용 경로 `/opt/dev-universe-blog`와 전용 Compose 프로젝트만 사용합니다. 릴리스 디렉터리를 만들고 current 심볼릭 링크를 교체합니다. 직전 링크는 `previous-release.txt`에 남깁니다. 빌드 실패 시 배포하지 않습니다. 최초 배포 전 기존 Docker provider/HTTPS entrypoint/letsencrypt resolver가 구성되어 있어야 합니다.

Traefik은 새 블로그 컨테이너의 도메인 전용 라벨을 자동 감지합니다. 기존 Traefik 및 다른 서비스의 파일이나 컨테이너는 변경하지 않습니다. 웹 컨테이너는 비관리자·읽기 전용으로 정적 결과물만 제공합니다. 포트를 호스트에 직접 공개하지 않습니다.

VPS MCP 개발 환경에서는 `/workspace/blog`를 편집·빌드할 수 있습니다. 운영 반영은 위 관리자 배포 명령을 사용합니다. MCP 환경에 Docker/root 권한을 추가하지 않습니다.

## 되돌리기

`/opt/dev-universe-blog`에서 `previous-release.txt`에 기록된 디렉터리를 확인하고 `site/current` 링크를 해당 릴리스로 교체합니다. 과거 릴리스는 자동 삭제하지 않습니다.

## 콘텐츠

첫 세 글은 블로그 시작과 개발 원칙을 소개하는 초기 콘텐츠입니다. 작성자 소개나 경력을 임의로 추가하지 않았습니다. 사용에 맞춰 자유롭게 수정하세요.

## 검색 및 AI 답변에서의 발견 가능성

페이지별 canonical, Open Graph/소셜 카드, WebSite·Person·BlogPosting·BreadcrumbList 구조화 데이터를 생성합니다. 소개 페이지에는 ProfilePage, 오류 페이지에는 noindex를 적용합니다. robots.txt는 검색 크롤러 접근을 허용하며 사이트맵과 RSS에는 공개 글만 포함됩니다. 별도의 AI 전용 파일이 검색 또는 인용을 보장하지는 않습니다.

발행할 때 핵심 질문과 짧은 답, 재현 환경, 실제 확인 결과, 한계와 공식 출처를 본문에 남기세요. 실제로 수행하지 않은 실험이나 경력을 추가하지 마세요. 수정일은 실질적인 본문 변경에만 사용하고 URL은 유지하세요. 제목·소개·요약은 글마다 고유하게 작성합니다.

```sh
npm run build
python3 scripts/check-seo.py
```

Search Console에서 색인 상태와 검색 실적을 확인합니다. 사이트맵 주소는 `https://dev-universe.tech/sitemap-index.xml`입니다. 검색 색인과 AI 답변의 인용은 외부 서비스가 결정하며, 배포 완료와 동일하지 않습니다.
