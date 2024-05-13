clear all;clc;close all;
thigh_55 = load("thigh055.mat").yy24(:,1:23);
thigh_83 = load('thigh083.mat').yy2(:,1:23);
thigh_110 = load('thigh110.mat').yy3(:,1:23);
thigh_138 = load('thigh138.mat').yy4(:,1:23);
knee_55 = load('knee055.mat').yy1(:,1:23);
knee_83 = load('knee083.mat').yy2(:,1:23);
knee_110 = load('knee110.mat').yy3(:,1:23);
knee_138 = load('knee138.mat').yy4(:,1:23);
ankle_55 = load('ankle055.mat').yy1(:,1:23);
ankle_83 = load('ankle083.mat').yy2(:,1:23);
ankle_110 = load('ankle110.mat').yy3(:,1:23);
ankle_138 = load('ankle138.mat').yy4(:,1:23);
q_thigh = [thigh_55,thigh_83,thigh_110,thigh_138];
writeNPY(q_thigh,'SpeedThigh.npy')
