#coding=utf-8;
import SimilarityAlgorithm as sa;
from bicluster import Bicluster;

def readfile(filename):
	lines = [line for line in open(filename)];
	
	#第一行是列标题：(单词列表)
	colnames = lines[0].strip().split('\t')[1:];
	#存放第一列，(博客主列表)
	rownames = [];
	#存放数据(每篇博客的单词频率)
	data = [];
	
	for line in lines[1:]:
		p = line.strip().split('\t');
		rownames.append(p[0]);
		data.append([float(x) for x in p[1:]]);
		
	return rownames,colnames,data;
	
def hcluster(rows,distance = sa.pearson):
	distances = {};
	currentclustid = -1;
	
	#最开始的聚类是数据集中的行
	clust = [Bicluster(rows[i],id = i) for i in range(len(rows))]; 
	
	while len(clust)>1:
		#相关度最紧密的一组序号
		lowestpair = (0,1);
		#存放这组的相关度
		closest = distance(clust[0].vec,clust[1].vec);
		
		#遍历每一个配对，寻找最小距离
		for i in range(len(clust)):
			for j in range(i+1,len(clust)):
				#用distances来缓存距离的计算值
				if(clust[i].id,clust[j].id not in distances):
					distances[(clust[i].id,clust[j].id)] = distance(clust[i].vec,clust[j].vec);
				d = distances[(clust[i].id,clust[j].id)];
				if(d < closest):
					closest = d;
					lowestpair = (i,j);
		
		#计算最近的两个聚类的平均值
		mergevec = [clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]/2.0 
		for i in range(len(clust[0].vec))];
		
		#建立新的聚类,ID为负数，表示是新生成的聚类
		newcluster = Bicluster(mergevec,left = clust[lowestpair[0]],
							   right = clust[lowestpair[1]],
							   distance = closest,id = currentclustid);
		
		#删除已被合并的聚类,原有聚类集合新增合并后的聚类
		currentclustid -= 1;
		del clust[lowestpair[1]];
		del clust[lowestpair[0]];
		clust.append(newcluster);
		
	return clust[0];

def printclust(clust,labels = None,n = 25):
	#利用缩进来建立层级布局
	for i in range(n): print(" ",end="");
	if(clust.id <0):
		#"oo"表示该聚类是一个分支
		print("oo");
	else:
		#正数表明该聚类是一个叶子节点
		if labels == None: return ;
		else : print(labels[clust.id]);
	
	#遍历左右子树
	if clust.left != None:
		printclust(clust.left,labels = labels , n = n-1);
	if clust.right != None:
		printclust(clust.right,labels = labels , n = n+1);
	

writersname,wordsname,wordscount = readfile("blogdata.txt");
clust = hcluster(wordscount);
printclust(clust,writersname);
