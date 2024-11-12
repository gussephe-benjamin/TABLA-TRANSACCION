import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    data = event['body']
    cuenta_origen = data['cuenta_origen']
    
    transaccion_table = dynamodb.Table('TablaTransacciones')
    
    try:
        response = transaccion_table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('cuenta_origen').eq(cuenta_origen)
        )
        
        return {
            'statusCode': 200,
            'body': response.get('Items', [])
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error al listar transacciones: {str(e)}'
        }
