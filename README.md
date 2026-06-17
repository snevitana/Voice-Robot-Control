# Voice Robot Control

Учебный прототип системы, которая распознаёт голосовые команды на русском языке и
преобразует их в управляющие команды для робота. Основной режим распознавания работает
локально через Vosk, без обязательного доступа к интернету.

## Архитектура

Проект разделён на независимые слои:

- `audio` - потоковый ввод аудио с микрофона.
- `speech` - распознавание речи через Vosk.
- `commands` - нормализация текста и сопоставление фраз с `RobotCommand`.
- `robot` - адаптеры отправки команд: simulation, serial, TCP.
- `config` - загрузка YAML-конфигурации.
- `cli` - пользовательские команды для запуска и проверки.

## Выбранный стек

- Python 3.11+.
- Vosk для офлайн-распознавания речи.
- sounddevice для аудиоввода.
- Typer и Rich для CLI.
- Pydantic и PyYAML для конфигурации.
- pyserial для интеграции с Arduino/контроллером.
- pytest, ruff, mypy для проверки качества.

## Установка на ПК

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

В PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

Если `sounddevice` не устанавливается на Linux/Raspberry Pi, установите системную
зависимость:

```bash
sudo apt install -y portaudio19-dev
```

## Загрузка модели Vosk

По умолчанию конфиги ожидают малую русскую модель:

```bash
./scripts/download_vosk_model.sh
```

Скрипт скачивает `vosk-model-small-ru-0.22` в директорию `models/`. Модели не
коммитятся в git. Если ссылка изменилась, скачайте актуальную русскую модель со
страницы Vosk Models и укажите путь в `vosk_model_path`.

## Запуск в режиме симуляции

```bash
voice-robot demo-text --text "стоп" --config configs/pc_simulation.yaml
```

Ожидаемый вывод:

```text
STOP
```

## Проверка сопоставления текстовой команды

```bash
voice-robot list-commands --config configs/pc_simulation.yaml
voice-robot test-match "поверни налево" --config configs/pc_simulation.yaml
```

## Запуск с микрофоном

Сначала скачайте модель Vosk, затем запустите:

```bash
voice-robot run --config configs/pc_simulation.yaml
```

Приложение слушает микрофон, распознаёт фразы и отправляет найденные команды в выбранный
backend. Неизвестные фразы пишутся в лог и не роняют приложение.

## Перенос на Raspberry Pi

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip portaudio19-dev
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
./scripts/download_vosk_model.sh
voice-robot demo-text --text "вперед" --config configs/raspberry_pi.yaml
voice-robot run --config configs/raspberry_pi.yaml
```

Для Raspberry Pi используется та же кодовая база. По умолчанию включён simulation
backend, чтобы можно было проверить цепочку без робота.

## Настройка serial backend

В `configs/raspberry_pi.yaml` поменяйте:

```yaml
backend: "serial"
serial:
  port: "/dev/ttyUSB0"
  baudrate: 9600
  timeout: 1.0
```

Проверьте доступные порты:

```bash
ls /dev/ttyUSB*
ls /dev/ttyACM*
```

Serial backend отправляет строки вида:

```text
MOVE_FORWARD
STOP
```

## Тестирование

```bash
ruff check .
ruff format .
pytest
mypy src
```

## Известные ограничения

- Качество распознавания зависит от микрофона и уровня шума.
- Словарь команд ограничен фразами из YAML-конфига.
- Точное сопоставление предсказуемо, но не исправляет ошибки распознавания.
- Малая модель Vosk быстрее на Raspberry Pi, но менее точна крупных моделей.
- Для serial backend нужны корректный порт и права доступа пользователя.

## Что можно улучшить дальше

- Добавить опциональный fuzzy matching через rapidfuzz.
- Добавить wake word перед выполнением команд.
- Реализовать ROS backend.
- Записывать историю команд в файл.
- Добавить метрики задержки распознавания.
