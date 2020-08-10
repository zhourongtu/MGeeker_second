create table user_info(
	id int not null,
    x_loc float,
    y_loc float,
    x_block int,
    y_block int,
    primary key(id),
    index(x_block, y_block)
);

create table user_info_test_1(
	id int not null,
    x_loc float,
    y_loc float,
    primary key(id)
);