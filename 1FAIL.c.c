#include <stdio.h>
/**Записываем в файл целые числа
Заменяем нечетные на противоположные
Гусятинер Л.Б., МГОТУ ККМТ, 26.11.2017 / КМПО РАНХиГС 30.03.2024
Задания.
Отсортировать файл "пузырьком"
Арутюнян С.К. 32ИС-21 01.04.24
**/

#include <stdio.h>

int main() {
    FILE * fh = fopen("1.dat", "wb+");
    int x = 0;
    long i, j;
    long isize = sizeof(int);
    long fsize;

    /// Запишем числа в файл
    for (i = 10; i > 0; i--)
        fwrite(&i, isize, 1, fh);

    /// Определим число записей в файле
    fseek(fh, 0, SEEK_END);
    fsize = ftell(fh) / sizeof(int);

    /// Отпечатаем содержимое файла до сортировки
    fseek(fh, 0, SEEK_SET);
    printf("Содержимое файла до сортировки: ");
    for (i=0; i<fsize; i++) {
        fread(&x, isize, 1, fh);
        printf("%d ", x);
    }
    putchar('\n');

    /// Сортировка файла методом пузырька
    for (i = 0; i < fsize - 1; i++) {
        for (j = 0; j < fsize - i - 1; j++) {
            int current, next;
            fseek(fh, j * isize, SEEK_SET);
            fread(&current, isize, 1, fh);
            fseek(fh, (j + 1) * isize, SEEK_SET);
            fread(&next, isize, 1, fh);
            if (current > next) {
                fseek(fh, j * isize, SEEK_SET);
                fwrite(&next, isize, 1, fh);
                fseek(fh, (j + 1) * isize, SEEK_SET);
                fwrite(&current, isize, 1, fh);
            }
        }
    }

    /// Отпечатаем содержимое файла после сортировки
    fseek(fh, 0, SEEK_SET);
    printf("Содержимое файла после сортировки: ");
    for (i=0; i<fsize; i++) {
        fread(&x, isize, 1, fh);
        printf("%d ", x);
    }
    putchar('\n');
    
    fclose(fh);
    return 0;
}
