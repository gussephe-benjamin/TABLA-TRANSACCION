import boto3
import json

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Parsear el cuerpo de la solicitud para obtener los datos
    data = json.loads(event['body'])
    cuenta_origen = data['cuenta_origen']
    transaccion_id = data['transaccion_id']
    
    # Referencia a la tabla de transacciones
    transaccion_table = dynamodb.Table('TablaTransacciones')
    
    try:
        # Obtener la transacción con cuenta_origen y transaccion_id
        response = transaccion_table.get_item(
            Key={
                'cuenta_origen': cuenta_origen,
                'transaccion_id': transaccion_id
            }
        )
        
        # Verificar si la transacción existe
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])  # Formatear en JSON
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Transacción no encontrada'})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error al obtener la transacción: {str(e)}'})
        }
