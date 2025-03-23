#!/bin/bash

# Agregar a .gitignore si no está
if ! grep -qxF "release_script_auto.sh" .gitignore; then
    echo "release_script_auto.sh" >> .gitignore
    echo "✅ Script añadido a .gitignore"
fi

# Hacer ejecutable
chmod +x release_script_auto.sh

# Detectar el último tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)

if [[ -z "$LAST_TAG" ]]; then
  echo "⚠️ No hay tags previos. Usando v1.0.0 como inicial."
  NEW_TAG="v1.0.0"
  GIT_RANGE=""
else
  echo "📌 Último tag: $LAST_TAG"

  # Obtener versión numérica
  VERSION=${LAST_TAG#v}
  IFS='.' read -ra PARTS <<< "$VERSION"
  MAJOR=${PARTS[0]}
  MINOR=${PARTS[1]}
  PATCH=${PARTS[2]}

  # Incrementar el patch
  PATCH=$((PATCH + 1))
  NEW_TAG="v$MAJOR.$MINOR.$PATCH"
  GIT_RANGE="$LAST_TAG..HEAD"
fi

echo "🔖 Nuevo tag: $NEW_TAG"

# Generar changelog desde último tag
echo "📝 Generando changelog..."
git log $GIT_RANGE --pretty=format:"- %s (%an)" > changelog.md

# Confirmar contenido
echo "📄 Contenido del changelog:"
cat changelog.md

# Commit del changelog
git add changelog.md
git commit -m "📄 Changelog para $NEW_TAG"

# Crear tag y hacer push
git tag $NEW_TAG
git push origin main
git push origin $NEW_TAG

# Crear release en GitHub
gh release create "$NEW_TAG" --title "$NEW_TAG" --notes-file changelog.md

echo "✅ Release $NEW_TAG creado y publicado exitosamente."