Пример. Троттлинг
Троттлинг (дословно "удушение") - снижение количества обрабатываемых запросов, относительно их общего количества. В примере предыдущего шага мы реализовали миддлварь, которая дропает вообще все апдейты от забаненных пользователей, но иногда нам нужно лишь дать понять пользователю, что если он будет слишком часто дергать бота, процесс не только не ускорится, но даже может замедлиться.

Тут нужно быть аккуратным, чтобы не вызывать у пользователей, корректно использующих бота, ощущения, что бот завис и больше не работает, потому еще надо продумать систему предупреждений. Но общий смысл работы троттлинг-миддлвари следующий. Берем какое-либо хранилище пар ключ-значение с возможностью установить время жизни ключа (Redis, NATS или даже просто TTLCache из библиотеки cachetools), при каждом апдейте от пользователя помещаем в хранилище его id (id юзера, а не апдейта) и устанавливаем время жизни для такого ключа. В миддлвари проверяем наличие ключа, закрепленного за пользователем, чей апдейт пришел в данный момент. Если ключа нет - добавляем ключ в хранилище и пропускаем апдейт дальше по цепочке обработки. А если ключ есть - просто дропаем апдейт. Хранилище само удалит ключ по истечении времени жизни этого ключа. Таким образом, будут обрабатываться не все апдейты пользователя, а только те, которые приходят не чаще определенного временного промежутка.