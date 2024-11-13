# TABLA-TRANSACCION
Aquí tienes los JSON para cada caso en la tabla **Transacción** de DynamoDB, basados en los requisitos que has especificado:

---

### 1. **POST - Crear Transacción**

Endpoint: `/transaccion/crear`

Este JSON crea una transacción, asegurando que ambas cuentas (origen y destino) existen y están asociadas con usuarios válidos.

#### Request JSON:
```json
{
  "usuario_origen": "user123",
  "cuenta_origen": "account12345",
  "usuario_destino": "user456",
  "cuenta_destino": "account67890",
  "monto": 1000
}
```

#### Expected Response JSON (Success):
```json
{
  "usuario_origen": "user123",
  "cuenta_origen": "account12345",
  "usuario_destino": "user456",
  "cuenta_destino": "account67890",
  "transaccion_id": "generated-uuid",
  "monto": 1000,
  "fecha_transaccion": "2024-11-13T12:00:00Z",
  "estado": "completada"
}
```

---

### 2. **DELETE - Eliminar Transacción**

Endpoint: `/transaccion/eliminar`

Este JSON elimina una transacción específica. Necesitas el `usuario_origen`, `cuenta_origen`, y el `transaccion_id` para identificar la transacción que deseas eliminar.

#### Request JSON:
```json
{
  "usuario_origen": "user123",
  "cuenta_origen": "account12345",
  "transaccion_id": "uuid-transaccion-1"
}
```

#### Expected Response JSON (Success):
```json
{
  "statusCode": 200,
  "body": "Transacción uuid-transaccion-1 eliminada con éxito"
}
```

---

### 3. **GET - Obtener Transacción**

Endpoint: `/transaccion/obtener`

Este JSON obtiene los detalles de una transacción específica usando el `usuario_origen`, `cuenta_origen`, y `transaccion_id`.

#### Request JSON:
```json
{
  "usuario_origen": "user123",
  "cuenta_origen": "account12345",
  "transaccion_id": "uuid-transaccion-1"
}
```

#### Expected Response JSON (If the transaction exists):
```json
{
  "usuario_origen": "user123",
  "cuenta_origen": "account12345",
  "usuario_destino": "user456",
  "cuenta_destino": "account67890",
  "transaccion_id": "uuid-transaccion-1",
  "monto": 1000,
  "fecha_transaccion": "2024-11-13T12:00:00Z",
  "estado": "completada"
}
```

#### Expected Response JSON (If the transaction does not exist):
```json
{
  "statusCode": 404,
  "body": "Transacción no encontrada"
}
```

---

### 4. **GET - Listar Transacciones**

Endpoint: `/transaccion/listar`

Este JSON lista todas las transacciones de una cuenta específica para un usuario. Necesitas el `usuario_origen` y `cuenta_origen`.

#### Request JSON:
```json
{
  "usuario_origen": "user123",
  "cuenta_origen": "account12345"
}
```

#### Expected Response JSON:
```json
[
  {
    "usuario_origen": "user123",
    "cuenta_origen": "account12345",
    "usuario_destino": "user456",
    "cuenta_destino": "account67890",
    "transaccion_id": "uuid-transaccion-1",
    "monto": 500,
    "fecha_transaccion": "2024-11-13T10:00:00Z",
    "estado": "completada"
  },
  {
    "usuario_origen": "user123",
    "cuenta_origen": "account12345",
    "usuario_destino": "user789",
    "cuenta_destino": "account54321",
    "transaccion_id": "uuid-transaccion-2",
    "monto": 750,
    "fecha_transaccion": "2024-11-13T11:00:00Z",
    "estado": "completada"
  }
]
```

---

### Explicación de los Campos

- **usuario_origen**: Representa el `usuario_id` del usuario que inicia la transacción desde su cuenta.
- **cuenta_origen**: Representa el `cuenta_id` asociado al `usuario_origen`, desde el cual se deduce el monto.
- **usuario_destino**: Representa el `usuario_id` del destinatario de la transacción.
- **cuenta_destino**: Representa el `cuenta_id` del destinatario de la transacción.
- **transaccion_id**: Es el identificador único de cada transacción (en el caso de obtener o eliminar una transacción específica).
- **monto**: La cantidad de dinero que se transfiere en la transacción.
- **fecha_transaccion**: Fecha y hora de la transacción, en formato ISO 8601.
- **estado**: Indica si la transacción fue `completada`, `pendiente`, o `fallida`.

---

Estos JSON ejemplos son adecuados para cada una de tus funciones Lambda y deberían ayudarte a realizar pruebas detalladas de cada caso en Postman.
