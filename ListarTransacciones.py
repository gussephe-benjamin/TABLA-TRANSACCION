import boto3
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Parsear el cuerpo de la solicitud
    data = json.loads(event['body'])
    cuenta_origen = data['cuenta_origen']
    
    # Referencia a la tabla de transacciones
    transaccion_table = dynamodb.Table('TablaTransacciones')
    
    try:
        # Consultar transacciones filtrando por cuenta_origen
        response = transaccion_table.query(
            KeyConditionExpression=Key('cuenta_origen').eq(cuenta_origen)
        )
        
        # Formatear la respuesta en JSON
        return {
            'statusCode': 200,
            'body': json.dumps(response.get('Items', []))
        }
    
    except Exception as e:
        # Responder con error en caso de excepción
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error al listar transacciones: {str(e)}'})
        }
