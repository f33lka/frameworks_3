# Чек‑лист проверки практики №15 (legacy-модуль)

1. Собрать и поднять стенд: `docker-compose build && docker-compose up -d`.
2. Убедиться, что контейнеры `iss_db`, `rust_iss`, `php_web`, `pascal_legacy`, `telemetry_cli`, `web_nginx` в статусе *running/healthy*.
3. Проверить `telemetry_legacy`:

   ```bash
   docker exec -it iss_db psql -U monouser -d monolith \
     -c "SELECT recorded_at, voltage, temp, source_file FROM telemetry_legacy ORDER BY recorded_at DESC LIMIT 5;"
   ```

   Ожидается несколько строк с `source_file = 'telemetry_cli'`.

4. Открыть `http://localhost:8080` и убедиться, что:
   * Dashboard загружается;
   * блоки CMS выводятся без SQL‑ошибок;
   * в секции CMS есть строка «Экспериментальный CMS‑блок для дашборда».

5. Перейти на страницы:

   * `http://localhost:8080/page/welcome`
   * `http://localhost:8080/page/unsafe`

   Проверить, что контент берётся из БД и отображается через шаблон `cms.page`.

6. Просмотреть логи:

   ```bash
   docker logs telemetry_cli --tail 20
   docker logs pascal_legacy --tail 20
   ```

   Для практики допустимо, что Pascal‑контейнер падает на unit `Process`, так как
   фактический поток данных обеспечивается `telemetry_cli`. Это отражено в отчёте.
