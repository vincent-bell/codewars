#include <stdlib.h>

int **multiplication_table(int n) {
	int **matrix=(int **) malloc (n*sizeof(int *));

	for(int i=0;i<n;i++){
		matrix[i]=(int *) malloc (n*sizeof(int));
		for(int j=0;j<n;j++)
			matrix[i][j]=(i+1)*(j+1);
	}

	return matrix;
}
