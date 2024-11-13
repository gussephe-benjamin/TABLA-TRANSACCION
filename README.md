# TABLA-TRANSACCION
Aquí tienes los JSON de cada caso para probar en Postman. Estos ejemplos incluyen información de usuario_id, cuenta_origen, y cuenta_destino. 

### 1. Crear Transacción (POST)

Este JSON crea una transacción, asegurando que ambas cuentas (origen y destino) existen y están asociadas con usuarios válidos.

json
{
  "usuario_origen": "user123",
  "cuenta_origen": "account12345",
  "usuario_destino": "user456",
  "cuenta_destino": "account67890",
  "monto": 1000
}


### 2. Eliminar Transacción (DELETE)

Este JSON elimina una transacción específica. Necesitas el usuario_origen, cuenta_origen, y el transaccion_id para identificar la transacción que deseas eliminar.

json
{
  "usuario_origen": "user123",
  "cuenta_origen": "account12345",
  "transaccion_id": "uuid-transaccion-1"
}


### 3. Obtener Transacción (GET)

Este JSON obtiene los detalles de una transacción específica usando el usuario_origen, cuenta_origen, y transaccion_id.

json
{
  "usuario_origen": "user123",
  "cuenta_origen": "account12345",
  "transaccion_id": "uuid-transaccion-1"
}


### 4. Listar Transacciones (GET)

Este JSON lista todas las transacciones de una cuenta específica para un usuario. Necesitas el usuario_origen y cuenta_origen.

json
{
  "usuario_origen": "user123",
  "cuenta_origen": "account12345"
}


### Explicación de Cada JSON y Su Relación con la Tabla de Cuentas y Usuarios

1. *usuario_origen* y *usuario_destino*: Representan el usuario_id del usuario propietario de cada cuenta, asegurando que la cuenta esté vinculada a un usuario válido.
2. *cuenta_origen* y *cuenta_destino*: Representan el cuenta_id asociado a cada usuario_id.
3. *transaccion_id*: Es el identificador único de cada transacción (en el caso de obtener o eliminar una transacción específica).
4. *monto*: La cantidad de dinero que se transfiere en la transacción.

### Uso de estos JSON en las Funciones Lambda

Cada función Lambda verificará que:

- *Crear Transacción*: Ambas cuentas (cuenta_origen y cuenta_destino) existen en la tabla de cuentas y están vinculadas a usuarios válidos (usuario_origen y usuario_destino). Además, verifica que el saldo en la cuenta_origen sea suficiente para cubrir el monto.
- *Eliminar Transacción*: La transacción especificada por el transaccion_id y cuenta_origen existe y pertenece al usuario_origen antes de eliminarla.
- *Obtener Transacción*: La función buscará la transacción especificada por el transaccion_id en la cuenta_origen del usuario_origen.
- *Listar Transacciones*: Listará todas las transacciones asociadas con la cuenta_origen del usuario_origen.

Esto asegura que las transacciones están correctamente asociadas con los usuarios y sus respectivas cuentas.
