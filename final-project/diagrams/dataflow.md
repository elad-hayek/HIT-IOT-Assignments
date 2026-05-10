# Data Flow Diagram - Message Processing

## Complete Message Flow

```mermaid
sequenceDiagram
    participant DHT as DHT Sensor<br/>(Living Room)
    participant BR as MQTT Broker<br/>(localhost:1883)
    participant MG as Data Manager<br/>(Central Processing)
    participant DB as SQLite<br/>Database
    participant GUI as GUI Dashboard
    participant RELAY as AC Relay

    Note over DHT,RELAY: Step 1: Sensor Data Collection
    DHT->>BR: Publish: home/living_room/dht<br/>{"temp":22.5,"humidity":55}

    Note over DHT,RELAY: Step 2: Manager Receives & Processes
    BR->>MG: Message Delivered (subscribed to home/#)
    MG->>MG: Parse JSON Message
    MG->>MG: Check Temperature Thresholds

    Note over DHT,RELAY: Step 3: Data Storage
    MG->>DB: INSERT iot_data<br/>(timestamp, DHT_LivingRoom, temperature, 22.5, °C)
    MG->>DB: INSERT iot_data<br/>(timestamp, DHT_LivingRoom, humidity, 55, %)

    Note over DHT,RELAY: Step 4: Alarm Detection (if needed)
    alt Temperature Warning Triggered
        MG->>BR: Publish: home/alerts/temperature<br/>{"severity":"warning",...}
    end

    Note over DHT,RELAY: Step 5: GUI Updates (1Hz Timer)
    GUI->>DB: Query: SELECT * FROM iot_data<br/>WHERE device_name='DHT_LivingRoom'<br/>ORDER BY timestamp DESC LIMIT 10
    DB->>GUI: Return latest sensor values
    GUI->>GUI: Update Display Labels & Colors

    Note over DHT,RELAY: Step 6: User Manual Control
    GUI->>GUI: User adjusts AC setpoint slider
    GUI->>BR: Publish: home/ac/control<br/>{"state":"HEATING","setpoint":24}

    Note over DHT,RELAY: Step 7: Actuator Response
    BR->>RELAY: Deliver Control Command
    RELAY->>RELAY: Update Relay State (ON/OFF)
    RELAY->>BR: Publish: home/ac/relay/status<br/>{"relay_state":"ON"}

    Note over DHT,RELAY: Step 8: GUI Alert Display
    BR->>GUI: Alert message received
    GUI->>GUI: Display in Alerts Panel
```

## Temperature Threshold Check Logic

```mermaid
flowchart TD
    A["Manager Receives<br/>Temperature Reading"] --> B{"Check Value<br/>Against Thresholds"}

    B -->|temp < 16°C| C["🔴 CRITICAL<br/>ALERT"]
    B -->|16°C ≤ temp < 18°C| D["🟠 WARNING"]
    B -->|18°C ≤ temp ≤ 28°C| E["🟢 NORMAL"]
    B -->|28°C < temp ≤ 32°C| F["🟠 WARNING"]
    B -->|temp > 32°C| G["🔴 CRITICAL<br/>ALERT"]

    C --> H["Log to Database<br/>with severity=alert"]
    D --> H
    E --> H
    F --> H
    G --> H

    C --> I["Publish Alert to<br/>home/alerts/temperature"]
    D --> I
    F --> I
    G --> I

    I --> J["GUI Receives Alert<br/>& Displays Message"]

    style C fill:#ff4444,color:#fff
    style D fill:#ffaa00,color:#000
    style E fill:#44aa44,color:#fff
    style F fill:#ffaa00,color:#000
    style G fill:#ff4444,color:#fff
```

## Database Schema

```mermaid
erDiagram
    IOT_DATA {
        int id PK "Primary Key - Auto Increment"
        string timestamp "ISO Format - 2026-05-10T14:30:45.123456"
        string device_name "DHT_Living_Room, DHT_Bedroom, Thermostat, AC_Relay"
        string sensor_type "temperature, humidity, state, setpoint, relay_state"
        real value "Numeric value (temp in C, humidity in %)"
        string unit "°C, %, ON/OFF"
        string severity "normal, warning, alert"
    }
```

## Example Data Records

```
id | timestamp                  | device_name        | sensor_type | value  | unit | severity
---|----------------------------|-------------------|-------------|--------|------|----------
 1 | 2026-05-10T14:30:45.123456 | DHT_Living_Room    | temperature | 22.5   | °C   | normal
 2 | 2026-05-10T14:30:45.234567 | DHT_Living_Room    | humidity    | 55.0   | %    | normal
 3 | 2026-05-10T14:30:50.345678 | DHT_Bedroom        | temperature | 20.8   | °C   | normal
 4 | 2026-05-10T14:30:50.456789 | DHT_Bedroom        | humidity    | 60.5   | %    | normal
 5 | 2026-05-10T14:30:55.567890 | Thermostat         | setpoint    | 22.0   | °C   | normal
 6 | 2026-05-10T14:30:55.678901 | AC_Relay           | relay_state | 0      | ON   | normal
 7 | 2026-05-10T14:30:50.000000 | ALERT_SYSTEM       | temperature_alarm | 0 | DHT_Bedroom | warning
```

## Latency Analysis

| Operation                              | Latency    | Notes                    |
| -------------------------------------- | ---------- | ------------------------ |
| Sensor → Broker                        | ~50ms      | Local network            |
| Broker → Manager                       | <10ms      | Instant subscription     |
| Manager Processing                     | ~20ms      | JSON parsing + DB insert |
| DB Storage                             | ~5ms       | SQLite write             |
| **Total: Sensor to DB**                | **~85ms**  | Sub-100ms storage        |
| GUI Query                              | ~10ms      | Simple SELECT query      |
| GUI Display Update                     | ~100ms     | PyQt5 render             |
| **Total: Sensor to GUI**               | **~195ms** | Sub-200ms visibility     |
| User Command to Relay                  | ~150ms     | Publish + receive        |
| **Total E2E: User Action to Actuator** | **~250ms** | Real-time control        |
