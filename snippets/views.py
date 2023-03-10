# import requests
# import time

# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response


# CLIENT_ID = 'local.6401c5074d90d2.81471623'
# CLIENT_SECRET = 'Eaig7HriyBq0SEB9ZamRl01SFs3bF3998lWthQAb15VxvvfZou'


# @api_view(['POST', 'GET'])
# def snippet_list(request, format=None):
#     global token
#     """
#     List all code snippets, or create a new snippet.
#     """
#     # if request.method == 'GET':
#     #     snippets = Snippet.objects.all()
#     #     serializer = SnippetSerializer(snippets, many=True)
#     #     return Response(serializer.data)
#     if request.method == 'GET':
#         print('GEEEEEEEEEEEEEEEEEEET')

#     if request.method == 'POST':
#         # Поиск по всем values
#         print('\n', 'AAAAA!!', request.POST, '\n')
#         if 'expired_token' in request.POST.getlist('error') or 'invalid_token' in request.POST.getlist('error'):
#             token = request.POST['auth[refresh_token]']
            
#             query_url = 'https://oauth.bitrix.info/oauth/token/'
#             query_data = {
#                 		'grant_type': 'refresh_token',
#                         'client_id': CLIENT_ID,
#                         'client_secret': CLIENT_SECRET,
#                         'refresh_token': token,
#             }
#             print('expired_token!', query_data, '\n')
            
#         else: 
#             token = request.POST['auth[access_token]']


#         if request.POST['event'] == 'ONAPPINSTALL':
#             # for i in request.POST:
#             #     print(i, request.POST[i])
#             # serializer = SnippetSerializer(data=request.data)
#             # PARAMS = {
#             #     'CODE' : 'itrbot',
#             #     'TYPE' : 'O',
#             #     'EVENT_HANDLER' : 'http://95.163.235.140:8005/snippets/',
#             #     # 'EVENT_MESSAGE_ADD' : 'http://95.163.235.140:8005/snippets/',
#             #     # 'EVENT_WELCOME_MESSAGE' : 'http://95.163.235.140:8005/snippets/',
#             #     # 'EVENT_BOT_DELETE' : 'http://95.163.235.140:8005/snippets/',
#             #     'OPENLINE' : 'Y',
#             #     'PROPERTIES' : {'NAME' : 'Python Telegram Bot 0',
#             #     'WORK_POSITION' : "Get bot for you open channel",
#             #     'COLOR' : 'RED'
#             #     },
#             #     'auth': token
#             # }
            
#             # url = request.POST['auth[client_endpoint]'] + 'imbot.register'
#             # x = requests.post(url, json = PARAMS)
#             # print('imbot.register', x.text)


#             PARAMS = {
#                 'ID': 'OL_0',
#                 'NAME': 'Коннектор к ОЛ 0',
#                 'ICON': {
#                     'DATA_IMAGE': r"data:image/svg+xml;charset=US-ASCII,%3Csvg%20version%3D%221.1%22%20id%3D%22Layer_1%22%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20x%3D%220px%22%20y%3D%220px%22%0A%09%20viewBox%3D%220%200%2070%2071%22%20style%3D%22enable-background%3Anew%200%200%2070%2071%3B%22%20xml%3Aspace%3D%22preserve%22%3E%0A%3Cpath%20fill%3D%22%230C99BA%22%20class%3D%22st0%22%20d%3D%22M34.7%2C64c-11.6%2C0-22-7.1-26.3-17.8C4%2C35.4%2C6.4%2C23%2C14.5%2C14.7c8.1-8.2%2C20.4-10.7%2C31-6.2%0A%09c12.5%2C5.4%2C19.6%2C18.8%2C17%2C32.2C60%2C54%2C48.3%2C63.8%2C34.7%2C64L34.7%2C64z%20M27.8%2C29c0.8-0.9%2C0.8-2.3%2C0-3.2l-1-1.2h19.3c1-0.1%2C1.7-0.9%2C1.7-1.8%0A%09v-0.9c0-1-0.7-1.8-1.7-1.8H26.8l1.1-1.2c0.8-0.9%2C0.8-2.3%2C0-3.2c-0.4-0.4-0.9-0.7-1.5-0.7s-1.1%2C0.2-1.5%2C0.7l-4.6%2C5.1%0A%09c-0.8%2C0.9-0.8%2C2.3%2C0%2C3.2l4.6%2C5.1c0.4%2C0.4%2C0.9%2C0.7%2C1.5%2C0.7C26.9%2C29.6%2C27.4%2C29.4%2C27.8%2C29L27.8%2C29z%20M44%2C41c-0.5-0.6-1.3-0.8-2-0.6%0A%09c-0.7%2C0.2-1.3%2C0.9-1.5%2C1.6c-0.2%2C0.8%2C0%2C1.6%2C0.5%2C2.2l1%2C1.2H22.8c-1%2C0.1-1.7%2C0.9-1.7%2C1.8v0.9c0%2C1%2C0.7%2C1.8%2C1.7%2C1.8h19.3l-1%2C1.2%0A%09c-0.5%2C0.6-0.7%2C1.4-0.5%2C2.2c0.2%2C0.8%2C0.7%2C1.4%2C1.5%2C1.6c0.7%2C0.2%2C1.5%2C0%2C2-0.6l4.6-5.1c0.8-0.9%2C0.8-2.3%2C0-3.2L44%2C41z%20M23.5%2C32.8%0A%09c-1%2C0.1-1.7%2C0.9-1.7%2C1.8v0.9c0%2C1%2C0.7%2C1.8%2C1.7%2C1.8h23.4c1-0.1%2C1.7-0.9%2C1.7-1.8v-0.9c0-1-0.7-1.8-1.7-1.9L23.5%2C32.8L23.5%2C32.8z%22/%3E%0A%3C/svg%3E%0A",
#                     'COLOR': '#1900ff',
#                     'SIZE': '90%',
#                     'POSITION': 'center'
#                 },
#                 'PLACEMENT_HANDLER': 'http://95.163.235.140:8005/snippets/',
#                 'auth': token
#             }
#             url = request.POST['auth[client_endpoint]'] + 'imconnector.register'
#             x = requests.post(url, json = PARAMS)
#             print('imconnector.register', x.text, '\n')


#             PARAMS = {
#                 'CONNECTOR': 'OL_0',
#                 'LINE': 3,
#                 'ACTIVE': 1,
#                 'auth': token
#             }

#             url = request.POST['auth[client_endpoint]'] + 'imconnector.activate'
#             x = requests.post(url, json = PARAMS)
#             print('imconnector.activate', x.text, '\n')


#             # PARAMS = {
#             #     'event': 'ONIMCONNECTORMESSAGEADD',
#             #     'handler': 'http://95.163.235.140:8005/snippets/',
#             #     'auth': token
#             # }
#             # url = request.POST['auth[client_endpoint]'] + 'event.bind'
#             # x = requests.post(url, json = PARAMS)
#             # print('event.bind', x.text)

#             PARAMS = {
#                 'CONNECTOR': 'OL_0',
#                 'LINE': 3,
#                 'MESSAGES': [{
                        
#                         'user': {
#                             'id': 3,
#                             'last_name': 'Иванов',
#                             'name': 'Иван',
#                         },
#                         'message': {
#                             'id': False,
#                             'date': int(time.time()),
#                             'text': '123'
#                         },
#                         'chat': {
#                             'id': 1
#                         }
                
#                 }],
#                 'auth': token
#             }
#             url = request.POST['auth[client_endpoint]'] + 'imconnector.send.messages'
#             x = requests.post(url, json = PARAMS)
#             print('imconnector.send.messages', x.text, '\n')

#             return Response({}, status=status.HTTP_201_CREATED)
        



#         # if request.POST['event'] == 'ONIMBOTMESSAGEADD':
#         #     print('ONIMBOTMESSAGEADD!!!', request.POST)    
#         #     PARAMS ={
#         #         'BOT_ID': request.POST['data[BOT][7][BOT_ID]'],
#         #         'DIALOG_ID': request.POST['data[PARAMS][DIALOG_ID]'],
# 		# 	    'MESSAGE': 'Function executed fffffff',
#         #         'auth': token
#         #     }
            
#         #     url = request.POST['auth[client_endpoint]'] + 'imbot.message.add'
#         #     # print(111, url)
#         #     x = requests.post(url, json = PARAMS)

#         return Response({}, status=status.HTTP_201_CREATED)
        
        


# # {'event': ['ONAPPINSTALL'], 'data[VERSION]': ['1'], 'data[ACTIVE]': ['Y'], 'data[INSTALLED]': ['Y'], 'data[LANGUAGE_ID]': ['ru'], 
# # 'ts': ['1677835663'], 'auth[access_token]': ['9fcb01640061cdde0061551a00000001000007d3618844bbe4f53815db20983f2e7e48'], 
# # 'auth[expires]': ['1677839263'], 'auth[expires_in]': ['3600'], 'auth[scope]': ['imopenlines,imbot,im,user'], 
# # 'auth[domain]': ['b24-la4wj9.bitrix24.ru'], 'auth[server_endpoint]': ['https://oauth.bitrix.info/rest/'], 
# # 'auth[status]': ['L'], 'auth[client_endpoint]': ['https://b24-la4wj9.bitrix24.ru/rest/'], 
# # 'auth[member_id]': ['e20f0e0c088c04ab1b71a5410309ddf3'], 'auth[user_id]': ['1'],
# #  'auth[refresh_token]': ['8f4a29640061cdde0061551a000000010000073dfbd604dd13f68fcf1ee3c2ee1f696c'], 
# #  'auth[application_token]': ['b6c563b7148a8912f4ad3ea159661c4c']}

# # {'event': ['ONIMBOTMESSAGEADD'], 'data[BOT][7][domain]': ['b24-bada6b.bitrix24.ru'], 
# # 'data[BOT][7][member_id]': ['e6c13a5fc0ea8379279efc4c504e2dea'], 
# # 'data[BOT][7][application_token]': ['c54784eb91e4985a507201de08986486'], 'data[BOT][7][AUTH][domain]': ['b24-bada6b.bitrix24.ru'], 
# # 'data[BOT][7][AUTH][member_id]': ['e6c13a5fc0ea8379279efc4c504e2dea'], 
# # 'data[BOT][7][AUTH][application_token]': ['c54784eb91e4985a507201de08986486'], 'data[BOT][7][BOT_ID]': ['7'], 
# # 'data[BOT][7][BOT_CODE]': ['itrbot'], 'data[PARAMS][FROM_USER_ID]': ['13'], 'data[PARAMS][MESSAGE]': ['Ро'], 
# # 'data[PARAMS][TO_CHAT_ID]': ['7'], 'data[PARAMS][MESSAGE_TYPE]': ['L'], 'data[PARAMS][SYSTEM]': ['N'], 
# # 'data[PARAMS][SKIP_COMMAND]': ['N'], 'data[PARAMS][SKIP_CONNECTOR]': ['N'], 'data[PARAMS][IMPORTANT_CONNECTOR]': ['N'], 
# # 'data[PARAMS][SILENT_CONNECTOR]': ['N'], 'data[PARAMS][AUTHOR_ID]': ['13'], 'data[PARAMS][CHAT_ID]': ['7'], 
# # 'data[PARAMS][CHAT_AUTHOR_ID]': ['0'], 'data[PARAMS][CHAT_ENTITY_TYPE]': ['LINES'], 
# # 'data[PARAMS][CHAT_ENTITY_ID]': ['telegrambot|1|786792821|13'], 'data[PARAMS][CHAT_ENTITY_DATA_1]': ['Y|DEAL|3|N|N|3|1678008993|0|0|0'], 
# # 'data[PARAMS][CHAT_ENTITY_DATA_2]': ['LEAD|0|COMPANY|0|CONTACT|3|DEAL|3'], 'data[PARAMS][CHAT_ENTITY_DATA_3]': [''], 
# # 'data[PARAMS][COMMAND_CONTEXT]': ['TEXTAREA'], 'data[PARAMS][MESSAGE_ORIGINAL]': ['Ро'], 'data[PARAMS][TO_USER_ID]': ['0'], 
# # 'data[PARAMS][DIALOG_ID]': ['chat7'], 'data[PARAMS][MESSAGE_ID]': ['51'], 'data[PARAMS][CHAT_TYPE]': ['L'], 
# # 'data[PARAMS][LANGUAGE]': ['ru'], 'data[USER][ID]': ['13'], 'data[USER][NAME]': ['ddos kim'], 'data[USER][FIRST_NAME]': ['ddos'], 
# # 'data[USER][LAST_NAME]': ['kim'], 'data[USER][WORK_POSITION]': [''], 'data[USER][GENDER]': ['M'], 'data[USER][IS_BOT]': ['N'], 
# # 'data[USER][IS_CONNECTOR]': ['Y'], 'data[USER][IS_NETWORK]': ['N'], 'data[USER][IS_EXTRANET]': ['Y'], 'ts': ['1678008994'], 
# # 'auth[access_token]': ['b27004640061cf480061cf440000000d000007218ed656fb4a04c1b1e3157fd693b1b0'], 'auth[expires]': ['1678012594'], 
# # 'auth[expires_in]': ['3600'], 'auth[scope]': ['imopenlines,imbot,im,user'], 'auth[domain]': ['b24-bada6b.bitrix24.ru'], 
# # 'auth[server_endpoint]': ['https://oauth.bitrix.info/rest/'], 'auth[status]': ['L'], 
# # 'auth[client_endpoint]': ['https://b24-bada6b.bitrix24.ru/rest/'], 'auth[member_id]': ['e6c13a5fc0ea8379279efc4c504e2dea'], 
# # 'auth[user_id]': ['13'], 'auth[refresh_token]': ['a2ef2b640061cf480061cf440000000d0000070f1afe85cd63bde5fba59bb0088fc4be'], 
# # 'auth[application_token]': ['c54784eb91e4985a507201de08986486']}>


# # @api_view(['GET', 'PUT', 'DELETE'])
# # def snippet_detail(request, pk, format=None):
# #     """
# #     Retrieve, update or delete a code snippet.
# #     """
# #     try:
# #         snippet = Snippet.objects.get(pk=pk)
# #     except Snippet.DoesNotExist:
# #         return Response(status=status.HTTP_404_NOT_FOUND)

# #     if request.method == 'GET':
# #         serializer = SnippetSerializer(snippet)
# #         return Response(serializer.data)

# #     elif request.method == 'PUT':
# #         serializer = SnippetSerializer(snippet, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# #     elif request.method == 'DELETE':
# #         snippet.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)