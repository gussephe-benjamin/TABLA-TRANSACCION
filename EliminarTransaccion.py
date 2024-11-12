import boto3
import json

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Parsear el cuerpo de la solicitud
    data = json.loads(event['body'])
    cuenta_origen = data['cuenta_origen']
    transaccion_id = data['transaccion_id']
    
    # Referencia a la tabla de transacciones
    transaccion_table = dynamodb.Table('TablaTransacciones')
    
    try:
        # Intentar eliminar el ítem con las claves especificadas
        transaccion_table.delete_item(
            Key={
                'cuenta_origen': cuenta_origen,
                'transaccion_id': transaccion_id
            }
        )
        
        # Responder con éxito si se elimina la transacción
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Transacción {transaccion_id} eliminada con éxito'})
        }
    
    except Exception as e:
        # Responder con error en caso de excepción
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error al eliminar la transacción: {str(e)}'})
        }
