#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COLLEGE_SIZE 1000

// Структура для хранения информации об успеваемости студентов
typedef struct {
    char group[20];
    char student[20];
    char discipline[20];
    double mark;
} Record;

// Структура для хранения информации о любимой дисциплине студента
typedef struct {
    char group[20];
    char student[20];
    char favorite_discipline[20];
} FavoriteRecord;

int main(void) {
    Record records[COLLEGE_SIZE]; // Массив записей об успеваемости студентов
    FavoriteRecord favorites[COLLEGE_SIZE]; // Массив для хранения информации о любимых дисциплинах студентов

    // Открытие входного файла
    FILE *in = fopen("in.txt", "r");
    if (in == NULL) {
        printf("Failed to open input file.\n");
        return 1;
    }

    int n = 0; // Счетчик количества записей
    char smark[20]; // Строка для временного хранения оценки
    // Считывание данных из входного файла в массив записей
    while (fscanf(in, "%s %s %s %s", records[n].student, records[n].group, records[n].discipline, smark) == 4) {
        records[n].mark = atof(smark); // Преобразование строки в число (оценку)
        n++;
    }
    fclose(in); // Закрытие входного файла

    // Находим любимую дисциплину для каждого студента
    int favorite_count = 0; // Счетчик для количества записей о любимых дисциплинах
    for (int i = 0; i < n; i++) {
        double max_mark = -1.0; // Начальное значение максимальной оценки
        int index = -1; // Индекс записи с максимальной оценкой для текущего студента
        for (int j = 0; j < n; j++) {
            if (strcmp(records[i].student, records[j].student) == 0) {
                if (records[j].mark > max_mark) {
                    max_mark = records[j].mark; // Обновляем максимальную оценку
                    index = j; // Обновляем индекс записи с максимальной оценкой
                }
            }
        }
        // Записываем информацию о любимой дисциплине для текущего студента
        if (index != -1) {
            strcpy(favorites[favorite_count].group, records[index].group);
            strcpy(favorites[favorite_count].student, records[index].student);
            strcpy(favorites[favorite_count].favorite_discipline, records[index].discipline);
            favorite_count++;
        }
        i = index; // Пропускаем записи, относящиеся к тому же студенту
    }

    // Сортируем записи о любимых дисциплинах по названию группы и фамилии студента
    for (int i = 0; i < favorite_count - 1; i++) {
        for (int j = 0; j < favorite_count - i - 1; j++) {
            if (strcmp(favorites[j].group, favorites[j + 1].group) > 0 ||
                (strcmp(favorites[j].group, favorites[j + 1].group) == 0 && strcmp(favorites[j].student, favorites[j + 1].student) > 0)) {
                FavoriteRecord temp = favorites[j];
                favorites[j] = favorites[j + 1];
                favorites[j + 1] = temp;
            }
        }
    }

    // Открываем выходной файл для записи результатов
    FILE *out = fopen("out.txt", "w");
    if (out == NULL) {
        printf("Failed to open output file.\n");
        return 1;
    }

    // Записываем результаты в выходной файл
    for (int i = 0; i < favorite_count; i++) {
        fprintf(out, "%s %s %s\n", favorites[i].group, favorites[i].student, favorites[i].favorite_discipline);
    }

    fclose(out); // Закрываем выходной файл

    return 0;
}
