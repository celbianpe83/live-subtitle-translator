#!/bin/bash

# Detectar el último tag
tags=$(git tag --sort=-creatordate)
last_tag=$(echo "$tags" | head -n 1)

# Si no hay tags, comenzamos desde v1.0.0
if [ -z "$last_tag" ]; then
  last_tag="v0.0.0"
fi

echo "📌 Último tag encontrado: $last_tag"

# Obtener commits desde el último tag
commits=$(git log $last_tag..HEAD --oneline)

if [ -z "$commits" ]; then
  echo "❌ No hay commits nuevos desde el último tag ($last_tag)."
  exit 0
fi

# Calcular el próximo tag (aumentar el parche)
version=$(echo "$last_tag" | sed 's/v//')
IFS='.' read -ra parts <<< "$version"
major=${parts[0]}
minor=${parts[1]}
patch=${parts[2]}
((patch++))
next_tag="v$major.$minor.$patch"

echo "🎉 Nuevo tag a crear: $next_tag"

# Crear changelog
echo "# Cambios en $next_tag" > changelog.md
echo "" >> changelog.md
git log $last_tag..HEAD --pretty=format:"- %s" >> changelog.md

# Commit changelog
git add changelog.md
git commit -m "docs: changelog para $next_tag"

# Crear tag
git tag $next_tag

echo "🔗 Pusheando commits y tag al repo"
git push origin main --tags

# Crear release
gh release create $next_tag \
  --title "$next_tag - Cambios recientes" \
  --notes-file changelog.md

echo "🚀 Release $next_tag publicado con éxito."
