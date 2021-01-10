# booking_office
Приложение должно предоставлять API, позволяющее осуществлять бронирование рабочих мест в кабинетах. 
API должно предоставлять ресурсы для:
* бронирования рабочих мест на определенный период времени; 
* просмотра списка бронирований по id рабочего места; 
* авторизации любым методом (Basic Auth годится) 
* ресурс рабочих мест должен иметь 2 необязательных параметра фильтрации: «datetime_from», «datetime_to», ожидающих datetime в формате ISO. 
Если данные валидны, то ответом на GET с указанными параметрами должен быть список рабочих мест, свободных в указанный временной промежуток.

## URLs ресурса

* api/registration/ регистрация пользователя
* api/auth/login/ 
* api/auth/logout/ 
* api/bookings/ все бронирования
* api/offices/ все места, админ может добавлять новые
* api/office/1/booking/ все брони места 1 и бронирование места на определенный период
* api/offices/free просмотр свободного места в заданный период <br>
(формат ввода `datetime_from=2021-01-08T13:00&datetime_to=2021-01-08T15:00`<br>
Например /api/offices/free?datetime_from=2021-01-08T13:00&datetime_to=2021-01-08T15:00)
