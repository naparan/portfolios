//インクルード
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

/*
- 方針 -

52枚のカード 
・ スペード・クラブ・ダイヤ・ハートの配列に13のカードを入れる
・ スペード(0~12),クラブ(13~25),ダイヤ(26~38),ハート(39,51)でカード番号を振る
・ カード番号からマーク・数字を求める(数値計算)
・ マーク番号：カード番号を13で割った商
・ 数字番号：カード番号をを13で割った余り + 1

52箇所のフィールド
・ 4×13行列（行：4,列：13）
・ 場ごとに番号を振る(0~51)
・ 番号：(行番号-1)×13+(列番号-1)
・ 行番号：番号を13で割った商 + 1 
・ 列番号：番号を13で割った余り + 1
*/



//カードを番号で管理する, num⇒数字番号,mark⇒マーク番号

    /*
    card⇒フィールドにあるカードの番号,front_back⇒表裏の管理

    front_backの表裏定義：
    表⇒1
    裏⇒0

    この場合、card変数からnum,markを求められる

    card型変数に表裏の管理変数を入れても良い
    */

struct field{
int card,front_back;
};

#define CARDS 52
int line=4,column=13;
struct field field[CARDS];

void disp(int cnt_correct, int left){
    //フィールド表示(関数化する⇒入力して再表示するから)
    int i,j;
    printf("   |");

    for(i=0;i<column;i++){
        printf("%3d ",i+1);
    }
    printf("\n---+----------------------------------------------------");
    
    for(i=0;i<line;i++){
	printf("\n%2d |",i+1);
	for(j=0;j<column;j++){
		if(field[i*13+j].front_back == 1){
                	switch (field[i*13+j].card/13){
                	case 0:
                    		printf("S");
                    		break;
                	case 1:
                    		printf("C");
                    		break;
                	case 2:
                    		printf("H");
                    		break;
                	case 3:
                    		printf("D");
                    		break;
                	default:
                    		break;
			}
                printf("%2d ",field[i*13+j].card%13+1);

                //表裏判定して表示を変更
                //表の場合：1,裏の場合：0
		} else {
                printf(" ?? ");
		}
        }
    }
   	printf("\n"); 
	printf("you have %d pairs\n",cnt_correct);
	printf("%d times the left\n",left);
}

void newlines(){
    int i;
    for(i=0;i<23;i++){
      	printf("\n");
    }
}

//入力関数（既に開いてるカードを選択したらエラーにする
int input(int num, int cnt_correct,int left){
    int x,y,field_num;
    char in[5];
    //入力を受け取る
    printf("input card%d x",num);
    fgets(in,5,stdin);
    x = atoi(in);
    if(x<1 || x>13){
	printf("Selected number out of line!\n");
	return input(num,cnt_correct,left);
    }

    printf("input card%d y",num);
    fgets(in,5,stdin);
    y = atoi(in);
    if(y<1 || y>4){
    	printf("Selected number out of line!\n");
    	return input(num,cnt_correct,left);
    }

    field_num = (y-1)*13+(x-1);
    if(field[field_num].front_back == 0){
        field[field_num].front_back = 1;
        newlines();
        disp(cnt_correct,left);
        return field_num;
    } else {
        printf("Selected a card that is already open!\n");
        printf("Please select again!\n");
        return input(num,cnt_correct,left);
    }
}

int main(){

    //入力情報変数
    char in[5];
    int x_1,y_1,x_2,y_2,field_num1,field_num2,cnt_correct=0,front;
    int i,j;

    //ランダム処理、フィールド番号の初期化
    srand(time(NULL));
    for(i=0;i<CARDS;i++){
        field[i].front_back = 1;
    }

    //カードのシャッフル
    i=0;
    while(i<CARDS){
        j=rand()%52;
        if(field[j].front_back == 1){
            field[j].card = i;
            field[j].front_back = 0;
            i++;
        }
    }


    i=50;
    while(i > -1){
        //最初の表示
        disp(cnt_correct,i);
        field_num1 = input(1,cnt_correct,i);
        field_num2 = input(2,cnt_correct,i);

        if(field[field_num1].card%13+1 == field[field_num2].card%13+1){
            printf("Correct!\n");
            cnt_correct++;
        } else {
            field[field_num1].front_back = 0;
            field[field_num2].front_back = 0;
	    printf("Incorrect!\n");
        }
	if(cnt_correct>=26){
		i=0;
		printf("You got all pairs!\n");
	}
        
        sleep(5);
        newlines(cnt_correct);
	i--;
    }

    //ゲームクリア
    if(cnt_correct==26){
	    printf("You win!\n");
	    printf("You cleared in %d times!\n",30-i+1);
    } else {
	    printf("Game over!\n");
	    printf("You got %d paires!\n",cnt_correct);
    }
    return 0;

}
