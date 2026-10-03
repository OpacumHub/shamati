#!/usr/bin/env bash
# Сборка фронта и выкладка в docroot прода.
# Запуск: bash deploy-frontend.sh   (из любой папки)

set -euo pipefail   # падать при любой ошибке, а не продолжать вслепую

# --- пути (поправь, если структура изменится) ---
CLIENT_DIR="/home/shadow/shamati/client"
DOCROOT="/var/www/www-root/data/www/shamati.zencodecraft.ru"
WEB_USER="www-root"

echo "==> 1/4 Сборка фронта"
cd "$CLIENT_DIR"
npm run build

# проверка, что сборка реально создалась (защита от выкладки пустоты)
if [ ! -f "$CLIENT_DIR/dist/index.html" ]; then
  echo "ОШИБКА: dist/index.html не найден — сборка не удалась. Деплой отменён."
  exit 1
fi

echo "==> 2/4 Очистка docroot"
sudo rm -rf "${DOCROOT:?}/"*     # :? — страховка: если DOCROOT пустой, rm не выполнится

echo "==> 3/4 Копирование сборки"
sudo cp -r "$CLIENT_DIR/dist/"* "$DOCROOT/"

echo "==> 4/4 Выставление владельца"
sudo chown -R "$WEB_USER:$WEB_USER" "$DOCROOT/"

echo "==> Готово. Проверь https://shamati.zencodecraft.ru/"