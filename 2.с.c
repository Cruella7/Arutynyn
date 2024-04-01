#include <stdio.h>
/// Записываем в файл целые числа
/// Заменяем нечетные на противоположные
/// Гусятинер Л.Б., МГОТУ ККМТ, 26.11.2017 / КМПО РАНХиГС 30.03.2024
/** Задания.
Отсортировать файл "выбором"
Арутюнян С.К. 32ИС-21 01.04.24
**/
int main() {
    FILE * fh = fopen("1.dat", "rb+");
    int x = 0;
    long i, j;
    long isize = sizeof(int);
    long fsize;

    // Определим число записей в файле
    fseek(fh, 0, SEEK_END);
    fsize = ftell(fh) / sizeof(int);

    // Чтение чисел из файла в массив
    int arr[fsize];
    fseek(fh, 0, SEEK_SET);
    for (i = 0; i < fsize; i++) {
        fread(&arr[i], isize, 1, fh);
    }

    // Сортировка массива методом выбора
    for (i = 0; i < fsize - 1; i++) {
        int min_index = i;
        for (j = i + 1; j < fsize; j++) {
            if (arr[j] < arr[min_index]) {
                min_index = j;
            }
        }
        // Обмен значениями
        int temp = arr[i];
        arr[i] = arr[min_index];
        arr[min_index] = temp;
    }

    // Запись отсортированных чисел обратно в файл
    fseek(fh, 0, SEEK_SET);
    for (i = 0; i < fsize; i++) {
        fwrite(&arr[i], isize, 1, fh);
    }

    // Печать содержимого файла
    fseek(fh, 0, SEEK_SET);
    for (i = 0; i < fsize; i++) {
        fread(&x, isize, 1, fh);
        printf("%d ", x);
    }
    putchar('\n');

    fclose(fh);
    return 0;
}
    return 0;