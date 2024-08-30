create database playMusica;

use playMusica;

create table musica(
   id_musica int primary key auto_increment not null,
   nome_musica varchar(50) not null,
   cantor_banda varchar(50) not null,
   genero_musica varchar(20) not null);
   
select * from musica;
   
insert into musica(nome_musica, cantor_banda, genero_musica) 
values('Todavia me alegrarei', 'Samuel Messias', 'Gospel');

insert into musica(nome_musica, cantor_banda, genero_musica) 
values('O sol', 'Vitor Kley', 'Pop');

insert into musica(nome_musica, cantor_banda, genero_musica) 
values('Cavalo de Troia', 'Mc Kelvin', 'Funk'),
('Isis', 'Mc Kako', 'Funk'), ('Pai é quem ria', 'Tierry', 'Sertanejo'),
('Lobo Guara', 'Hungria', 'Rap'), ('Meu abrigo', 'Mellin', 'Popp');

select * from musica where cantor_banda like 'M%';

update musica set cantor_banda = 'Melin', genero_musica = 'Pop' where id_musica = 5;

create table usuario(
   id_usuario int primary key auto_increment,
   nome_usuario varchar(50) not null,
   login_usuario varchar(50) not null,
   senha_usuario varchar(15) not null);
   
insert into usuario(nome_usuario, login_usuario, senha_usuario) 
values('Daniel Xavier', 'daniel.xds93', 'admin');

insert into usuario(nome_usuario, login_usuario, senha_usuario) 
values('Vilma Nunes', 'vilmanunes104', 'nunes');

select * from usuario;

alter table usuario 
add unique(login_usuario);
truncate table usuario;

insert into usuario(nome_usuario, login_usuario, senha_usuario) 
values('Daniel Xavier', 'daniel.xds93', 'admin'),
('Vilma Nunes', 'vilmanunes104', 'nunes'),
('Daniel Xavier Santos', 'daniel.xds94', 'admin');
insert into usuario(nome_usuario, login_usuario, senha_usuario) 
values('Danielle', 'dani', 'dani');