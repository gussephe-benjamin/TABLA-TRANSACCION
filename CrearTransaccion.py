import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    data = event['body']  # Asumiendo que los datos están en el body de la solicitud
    cuenta_origen = data['cuenta_origen']
    cuenta_destino = data['cuenta_destino']
    monto = data['monto']
    
    # Generar un ID único para la transacción
    transaccion_id = str(uuid.uuid4())
    
    # Referencias a las tablas
    transaccion_table = dynamodb.Table('TABLA-TRANSACCION')
    cuenta_table = dynamodb.Table('TABLA-CUENTA')

    # Verificar saldo en cuenta origen
    cuenta_origen_data = cuenta_table.get_item(Key={'usuario_id': cuenta_origen})
    if 'Item' not in cuenta_origen_data or cuenta_origen_data['Item']['saldo'] < monto:
        return {
            'statusCode': 400,
            'body': 'Fondos insuficientes en cuenta origen'
        }
    
    try:
        # Actualizar los saldos en las cuentas origen y destino
        cuenta_table.update_item(
            Key={'usuario_id': cuenta_origen},
            UpdateExpression="SET saldo = saldo - :monto",
            ExpressionAttributeValues={':monto': monto}
        )
        cuenta_table.update_item(
            Key={'usuario_id': cuenta_destino},
            UpdateExpression="SET saldo = saldo + :monto",
            ExpressionAttributeValues={':monto': monto}
        )
        
        # Registrar la transacción en la tabla de transacciones
        transaccion_table.put_item(
            Item={
                'transaccion_id': transaccion_id,
                'cuenta_origen': cuenta_origen,
                'cuenta_destino': cuenta_destino,
                'monto': monto,
                'fecha_transaccion': datetime.utcnow().isoformat(),
            }
        )
        
        return {
            'statusCode': 200,
            'body': f'Transacción {transaccion_id} realizada con éxito'
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error al realizar la transacción: {str(e)}'
        }
