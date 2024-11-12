import boto3
import uuid
from datetime import datetime
import json

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    data = json.loads(event['body'])  # Convertir el cuerpo del evento de JSON a un diccionario de Python
    usuario_origen = data['usuario_origen']
    cuenta_origen = data['cuenta_origen']
    usuario_destino = data['usuario_destino']
    cuenta_destino = data['cuenta_destino']
    monto = data['monto']
    
    # Generar un ID único para la transacción
    transaccion_id = str(uuid.uuid4())
    
    # Referencias a las tablas
    transaccion_table = dynamodb.Table('TABLA-TRANSACCION')
    cuenta_table = dynamodb.Table('TABLA-CUENTA')
    usuario_table = dynamodb.Table('TABLA-USUARIO')

    # Verificar que las cuentas de origen y destino existen y pertenecen a los usuarios indicados
    cuenta_origen_data = cuenta_table.get_item(Key={'usuario_id': usuario_origen, 'cuenta_id': cuenta_origen})
    cuenta_destino_data = cuenta_table.get_item(Key={'usuario_id': usuario_destino, 'cuenta_id': cuenta_destino})

    if 'Item' not in cuenta_origen_data:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Cuenta de origen no encontrada para el usuario de origen'})
        }
    
    if 'Item' not in cuenta_destino_data:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Cuenta de destino no encontrada para el usuario de destino'})
        }

    # Verificar saldo en cuenta origen
    saldo_origen = cuenta_origen_data['Item']['saldo']
    if saldo_origen < monto:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Fondos insuficientes en cuenta de origen'})
        }
    
    try:
        # Actualizar los saldos en las cuentas origen y destino
        cuenta_table.update_item(
            Key={'usuario_id': usuario_origen, 'cuenta_id': cuenta_origen},
            UpdateExpression="SET saldo = saldo - :monto",
            ExpressionAttributeValues={':monto': monto}
        )
        
        cuenta_table.update_item(
            Key={'usuario_id': usuario_destino, 'cuenta_id': cuenta_destino},
            UpdateExpression="SET saldo = saldo + :monto",
            ExpressionAttributeValues={':monto': monto}
        )
        
        # Registrar la transacción en la tabla de transacciones
        transaccion_table.put_item(
            Item={
                'transaccion_id': transaccion_id,
                'usuario_origen': usuario_origen,
                'cuenta_origen': cuenta_origen,
                'usuario_destino': usuario_destino,
                'cuenta_destino': cuenta_destino,
                'monto': monto,
                'fecha_transaccion': datetime.utcnow().isoformat(),
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Transacción {transaccion_id} realizada con éxito'})
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error al realizar la transacción: {str(e)}'})
        }
