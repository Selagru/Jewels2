������� ��������� (������):
	� ��������� �������� � ����� ������� �������� ���������������:
		docker-compose run web python /code/manage.py migrate --noinput
		docker-compose run web python /code/manage.py createsuperuser --username admin --email q@q.com
		docker-compose up -d --build


������ ���������� �������: docker-compose up


������ ����� ��� ���������:
	1.�������� ����� ��� ���������:
		a. https://127.0.0.1:8000/upload/ - ���� ����������� ��������� ��� �������� ������ � ������� ���������� ���������.
			��������� ����������:
				"���� �� ������� �������" - �� ������ ��� �����.
				"���� �����������" - �� ������ ����.
				"��������� ������ �� ���� ���������� �� �� ������ � ���:{errors}" - CSV ���� ��������� �� ���������, ������ � �������� ��������� � ���� ������.
				"OK - ���� ��� ��������� ��� ������" - �� �������.

		b. ������ ����� Insomnia / Postman �� https://127.0.0.1:8000/upload/ (��������� ������: POST)
			Content-Type: multipart/form-data
			�����: deals - "����.csv"

	2. ������ ������������ ������:
		https://127.0.0.1:8000/top_5_customers/ (��������� ������: GET) - ���������� ������ �����������, ������� ��������� ������ ����� + ������ ������, �������� �������.
		(������ ���������� �� 15 �����)


��� �� ������� ������� �� ������ https://127.0.0.1:8000/admin/ � ������� ����� ����������:
	�������������,
	������ (� ������������ ������ �� ��������� �����: ['customer', 'item', 'date'],
	����� (� ������������ ������ �� ��������).


�������� ������� ������ � ��������:
	1. �� ������ https://127.0.0.1:8000/upload/ - ��������� CSV ����.
	2. �� ������ https://127.0.0.1:8000/top_5_customers/ - ������� ��� 5 ������� � �� ������� �����.
	3. �� ������ https://127.0.0.1:8000/admin/ - ��������.