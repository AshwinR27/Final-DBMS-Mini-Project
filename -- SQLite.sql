-- SQLite
create table if not exists route(
     route_id integer primary key autoincrement,
     source varchar2(20),
    destination varchar2(20),
   fare number(10,2) NOT NULL,
   distance varchar2(10),
   time varchar2(10));

INSERT INTO route (source, destination,fare,distance,time)
VALUES ('Bangalore','Mysore',3993.90,'143.8km','3hr 27min');
INSERT INTO route (source, destination,fare,distance,time)
VALUES ('Bangalore','Mangalore',7441.59,'351.8km','7hr 58min');
INSERT INTO route (source, destination,fare,distance,time)
VALUES ('Bangalore','Chennai',5499.00,'345.7km','6hr 32min');
INSERT INTO route (source, destination,fare,distance,time)
VALUES ('Bangalore','Telangana',14990.00,'715.5km','11hr 32min');

INSERT INTO route (source, destination,fare,distance,time)
VALUES ('Mangalore','Mumbai',14350.90,'893.3km','16hr 32min');
INSERT INTO route (source, destination,fare,distance,time)
VALUES ('Mangalore','Bangalore',7441.59,'351.8km','7hr 58min');
INSERT INTO route (source, destination,fare,distance,time)
VALUES ('Mangalore','Chennai',20499.00,'705.0km','14hr 13min');


drop TABLE driver

DELETE  from driver where driver_id=101

create TABLE driver(
driver_id integer PRIMARY KEY,
Dname varchar2(20) NOT NULL,
DL_no number(10) UNIQUE NOT NULL,
dph_no number(10) NOT NULL,
Age number(2),
admin_id REFERENCES admin(admin_id) DEFAULT 101);

INSERT into driver VALUES(101,'Arman Malik','A4329LF4J49042J',
9440487109,23,101);
INSERT into driver VALUES(102,'Rohan Sharma','JF30FO381JD914F',
89319037495,44,101);
INSERT into driver
VALUES(103,'Rahul K','DKW029099EK2KD2',
9903199103,32,101);
INSERT into driver
VALUES(104,'Rajesh Sharma','12J9EO10DL33J4F',
89109893813,45,101);
INSERT into driver
VALUES(105,'Ronit R','A92K2801OE350C3',
9201113031,45,101);
INSERT into driver
VALUES(106,'Raj Kapoor','29DEO10EPC14EKD',
7718304194,32,101);
INSERT into driver
VALUES(107,'Aryan Khan','381LE01EAD9238F',
9120314451,35,101);
INSERT into driver
VALUES(108,'Rohan Joshi','1JD919DN4501PCV',
9998110384,29,101);

create table cab(
type varchar2(15) NOT NULL,
Driver_id REFERENCES driver(driver_id),
reg_no varchar2(15) NOT NULL,
PRIMARY KEY(Driver_id,reg_no)); 

INSERT INTO cab VALUES('SUV',101,'KA19P1234');
INSERT INTO cab VALUES('Sedan',102,'KA19MH1230');
INSERT INTO cab VALUES('Minivan',103,'KA03P0089');
INSERT INTO cab VALUES('Hatchback',104,'KA01P1345');
INSERT INTO cab VALUES('SUV',105,'MH93P1491');
INSERT INTO cab VALUES('Sedan',106,'KA29PG314');
INSERT INTO cab VALUES('SUV',107,'KA38N2910');

drop table Booking;

create table Booking(
booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
customer_id REFERENCES customer(customer_id),
route_id REFERENCES route(route_id),
reg_no REFERENCES Cab(reg_no),
driver_id REFERENCES CAB(driver_id),
total_fare number(10,2) not null,
status varchar2(20) default 'ACTIVE' not null);


INSERT INTO Booking (route_id,reg_no,driver_id,total_fare) VALUES(2,'KA38N2910',107,7441.59);

DELETE FROM Booking where booking_id = 55

DELETE FROM booking where 1<2

select route_id,customer_id,driver_id from Booking where customer_id='1427'

select count(*) from booking where customer_id='1427'

select driver_id,reg_no from cab where type='SUV' and Avail='No'

select type from cab where driver_id = 103

alter table driver add admin_id REFERENCES admin(admin_id) on delete set DEFAULT ;

alter table driver add constraint def default '101' for admin_id;

drop table cab;

DROP TABLE CUSTOMER;

create table customer(
customer_id integer primary key autoincrement,
username varchar2(20) unique,
pwd varchar2(20) not null,
name varchar2(40) not null,
ph_no number(10),
email varchar2(40)
);

INSERT INTO CUSTOMER VALUES (1420,'Flast','1234','First Last','1234567890','Flast@gmail.com');