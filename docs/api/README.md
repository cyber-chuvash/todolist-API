# API documentation
This is a documentation for the REST API of my [TODO-list project](https://github.com/cyber-chuvash/todolist-API).

This markdown document was converted from a [swagger spec](https://github.com/cyber-chuvash/todolist-API/blob/master/docs/api/todolist-API-swagger.yml) using [swagger-markdown](https://github.com/syroegkin/swagger-markdown). **Hence this document is kinda scuffed.** 

Please refer to the original rendered with swagger-ui: [docs.todo.chuvash.pw](https://docs.todo.chuvash.pw/)


## Version: 0.1.0

**Contact information:**  
Mikhail Migushov  
m.migushov@gmail.com  

**License:** [MIT license](https://github.com/cyber-chuvash/todolist-API/blob/master/LICENSE)

### Security
**api_key**  

|apiKey|*API Key*|
|---|---|
|Description|Until auth flow is created, the value for this token == user_id|
|Name|api_key|
|In|header|

### /users/{user_id}

#### GET
##### Summary:

Get info about user

##### Description:

Return info about the user

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
|  |  |  | No | [userIdParam](#userIdParam) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | User was found | [User](#User) |
| 404 | User not found |  |

### /lists/

#### GET
##### Summary:

Get an array of available TODO-lists

##### Description:

Return a paginated view on TODO-lists available to the user

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| limit | query |  | No | [limitParam](#limitParam) |
| offset | query |  | No | [offsetParam](#offsetParam) |
| include_cards | query | Whether to include an array of cards associated with the lists | No | boolean |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Success (array MAY be empty). If include_cards parameter is set to true, there will also be an array of cards for each list (see [GET /lists/<list_id>](#/lists/get_lists__list_id_)). | [ [TodoList](#TodoList) ] |

#### POST
##### Summary:

Create a new TODO-list

##### Description:

Create a new TODO-list for the user

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| body | body | Body describes a new TODO-list object | Yes | [NewTodoList](#NewTodoList) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Successfully created a list | [TodoList](#TodoList) |
| 401 | You don't have access to create lists for this user |  |

### /lists/{list_id}

#### GET
##### Summary:

Get info about a TODO-list

##### Description:

Return info about the list and it's cards

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| list_id | path | ID of the list | Yes | long |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Found the list | [VerboseTodoList](#VerboseTodoList) |
| 401 | You don't have access to this list |  |
| 404 | List not found |  |

#### PATCH
##### Summary:

Update a TODO-list

##### Description:

Update info about a TODO-list

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| list_id | path | ID of the list | Yes | long |
| body | body | Fields from a TODO-list object that need to be updated with new values. | Yes | [NewTodoList](#NewTodoList) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Updated the list | [TodoList](#TodoList) |
| 401 | You don't have access to this list |  |
| 404 | List not found |  |

#### DELETE
##### Summary:

Delete a TODO-list

##### Description:

Delete an entire TODO-list, including all it's cards

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| list_id | path | ID of the list | Yes | long |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successfully deleted the list |
| 401 | You don't have access to this list |
| 404 | List not found |

### /lists/{list_id}/cards/

#### POST
##### Summary:

Create a new card in a list

##### Description:

Create a new card in a list

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| list_id | path | ID of the list | Yes | long |
| body | body | Body describes a new card object | Yes | [NewCard](#NewCard) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Successfully created a card | [Card](#Card) |
| 401 | You don't have access to create cards in this list |  |
| 404 | List not found |  |

### /lists/{list_id}/cards/{card_id}

#### GET
##### Summary:

Get a single card info

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| list_id | path | ID of the list | Yes | long |
| card_id | path | ID of the card | Yes | long |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Info about a card | [Card](#Card) |
| 401 | You don't have access to cards in this list |  |
| 404 | List or card are not found |  |

#### PATCH
##### Summary:

Update a card

##### Description:

Update a card

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| list_id | path | ID of the list | Yes | long |
| card_id | path | ID of the card | Yes | long |
| body | body | Fields from a card object that need to be updated with new values. | Yes | [NewCard](#NewCard) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Successfully updated the card | [Card](#Card) |
| 401 | You don't have access to update cards in this list |  |
| 404 | List or card are not found |  |

#### DELETE
##### Summary:

Delete a card

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| list_id | path | ID of the list | Yes | long |
| card_id | path | ID of the card | Yes | long |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successfully deleted the card |
| 401 | You don't have access to delete cards from this list |
| 404 | List or card are not found |

### /account/

#### GET
##### Summary:

Get current user's account

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Returned info about current user's account | [Account](#Account) |
| 401 | Login required |  |

#### POST
##### Summary:

Create a new account

##### Description:

Register a new user account

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| body | body |  | Yes | [NewAccount](#NewAccount) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Successfully created a new user account | [Account](#Account) |

#### DELETE
##### Summary:

Delete current user's account

##### Description:

Completely delete current users account with all of the lists associated with it. 

#### *THIS ACTION IS IRREVERSIBLE.*

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | The account was successfully deleted |

### Models


#### _BaseUser

Base user object, for inheritance only

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| username | string |  | Yes |

#### User

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| User |  |  |  |

#### NewAccount

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| NewAccount |  |  |  |

#### Account

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| Account |  |  |  |

#### NewTodoList

A new TODO-list object

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| title | string |  | Yes |

#### TodoList

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| TodoList |  |  |  |

#### VerboseTodoList

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| VerboseTodoList |  |  |  |

#### NewCard

A new card in a TODO-list

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| text | string |  | Yes |
| description | string |  | No |
| is_done | boolean |  | No |

#### Card

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| Card |  |  |  |

#### genericId

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| genericId | integer |  |  |

#### userIdParam

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| userIdParam |  |  |  |

#### limitParam

A maximum number of objects to return

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| limitParam | integer | A maximum number of objects to return |  |

#### offsetParam

A number of objects to skip over

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| offsetParam | integer | A number of objects to skip over |  |