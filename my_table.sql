create table user_info(
	id int not null,
    x_loc float,
    y_loc float,
    x_block int,
    y_block int,
    index(x_block, y_block)
);
