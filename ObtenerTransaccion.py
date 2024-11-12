import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    data = event['body']
    cuenta_origen = data['cuenta_origen']
    transaccion_id = data['transaccion_id']
    
    transaccion_table = dynamodb.Table('TablaTransacciones')
    
    try:
        response = transaccion_table.get_item(
            Key={
                'cuenta_origen': cuenta_origen,
                'transaccion_id': transaccion_id
            }
        )
        
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': response['Item']
            }
        else:
            return {
                'statusCode': 404,
                'body': 'Transacción no encontrada'
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error al obtener la transacción: {str(e)}'
        }
