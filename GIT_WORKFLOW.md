# GIT WORKFLOW

Guia rapida para trabajar en este repositorio de forma segura y compatible en cualquier OS.

## 1) Flujo diario (rapido)

```bash
git pull
git add .
git commit -m "tipo: mensaje claro"
git push
```

Ejemplos de tipo:
- `feat`: nueva funcionalidad
- `fix`: correccion de bug
- `chore`: tareas tecnicas
- `docs`: documentacion
- `refactor`: mejora interna sin cambiar comportamiento

## 2) Flujo recomendado con rama feature

```bash
git pull
git checkout -b feature/nombre-cambio
```

Haz cambios y luego:

```bash
git add .
git commit -m "feat: agrega X para resolver Y"
git push
```

Cuando termines, abre Pull Request en GitHub hacia `main`.

## 3) Publicar en GitHub Pages

Este repositorio publica en:

- `https://henrystark866.github.io/Educando866/`

Pasos:
1. Sube cambios a `main`.
2. En GitHub, ve a **Settings > Pages**.
3. Verifica que la fuente sea `Deploy from a branch` con rama `main` y carpeta `/ (root)`.

## 4) Comandos utiles

```bash
git status
git log --oneline --decorate -n 10
git diff
git branch
git switch main
```

## 5) Buenas practicas

- Haz `git pull` antes de empezar.
- Usa mensajes de commit cortos y claros.
- Evita subir secretos (tokens, claves, `.env`).
- Si hay conflicto, resuelvelo localmente y vuelve a hacer `git add`, `git commit`, `git push`.
