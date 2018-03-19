#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

const int Move_Probability = 50;
const int Direction_Probability = 50;

typedef struct
{
  int Role;
  int Is_Tore;
  int N;
  int Hunters_Count;
  int Victum_Steps;
  int Max_Steps;
  int Cur_Step;
} Game_Rules;

typedef struct
{
  int X;
  int Y;
} Point;

typedef struct
{
  int Count;
  Point * Points;
} Shift;

void ReadSituation(char * file_name, Game_Rules * rules, Point ** hunters, Point * victum)
{
  FILE * fp = fopen(file_name, "r");

  // Read rules
  fscanf(fp, "%d", &rules->Role);
  fscanf(fp, "%d", &rules->Is_Tore);
  fscanf(fp, "%d", &rules->N);
  fscanf(fp, "%d", &rules->Hunters_Count);
  fscanf(fp, "%d", &rules->Victum_Steps);
  fscanf(fp, "%d", &rules->Max_Steps);
  fscanf(fp, "%d", &rules->Cur_Step);

  // Read victum coordinates
  fscanf(fp, "%d", &victum->X);
  fscanf(fp, "%d", &victum->Y);

  // Allocated hunters coordinates
  *hunters = (Point *)malloc(rules->Hunters_Count * sizeof(Point));

  Point * pt_hunters = *hunters;

  // Read hunters coordinates
  for (int i = 0; i < rules->Hunters_Count; ++i)
  {
    fscanf(fp, "%d", &pt_hunters[i].X);
    fscanf(fp, "%d", &pt_hunters[i].Y);
  }

  fclose(fp);
}

void SetStartPosition(Point * point, int dimention)
{
  point->X = rand() % dimention;
  point->Y = rand() % dimention;
}

void CheckBorders(Point * point, Point * shift, int is_tore, int dimention)
{
  if (is_tore == 0)
  {
    if (point->X + shift->X > dimention)
    {
      shift->X *= -1;
    }

    if (point->Y + shift->Y > dimention)
    {
      shift->Y *= -1;
    }
  }
}

void TakeStep(Point * shift)
{
  shift->X = 0;
  shift->Y = 0;

  int move_or_stay = (rand() % 100) < Move_Probability;
  int horizontally_or_vertically = (rand() % 100) < Direction_Probability;

  if (move_or_stay == 1)
  {
    if (horizontally_or_vertically == 1)
    {
      int rigth_or_left = (rand() % 100) < Direction_Probability;

      shift->X = rigth_or_left == 1 ? 1 : -1;
    }
    else
    {
      int up_or_down = (rand() % 100) < Direction_Probability;

      shift->Y = up_or_down == 1 ? 1 : -1;
    }
  }
}

void CalculateSteps(Game_Rules * rules, Shift * shifts, Point * hunters, Point * victum)
{
  shifts->Count = rules->Role == 1
    ? rules->Cur_Step != 0 ? rules->Victum_Steps : 1
    : rules->Hunters_Count;

  shifts->Points = (Point *)malloc(shifts->Count * sizeof(Point));

  if (rules->Cur_Step == 0)
  {
    for (int i = 0; i < shifts->Count; ++i)
    {
      SetStartPosition(&shifts->Points[i], rules->N);
    }
  }
  else
  {
    for (int i = 0; i < shifts->Count; ++i)
    {
      Point * point = rules->Role == 0 ? &hunters[i] : victum;
      Point * shift = &shifts->Points[i];

      TakeStep(shift);
      CheckBorders(point, shift, rules->Is_Tore, rules->N);

      point->X += shift->X;
      point->Y += shift->Y;
    }
  }
}

void WriteSteps(char * file_name, Shift * shifts)
{
  FILE * fp = fopen(file_name, "w");

  for (int i = 0; i < shifts->Count; ++i)
  {
    fprintf(fp, "%d %d\n", shifts->Points[i].X, shifts->Points[i].Y);
  }

  fclose(fp);
}

int main(int argc, char ** argv)
{
  if (argc < 3)
  {
    printf("Need more arguments!!!\n");
    return 1;
  }

  Game_Rules rules;
  Point victum;
  Point * hunters;

  Shift shift_points;

  srand(time(NULL));

  ReadSituation(argv[1], &rules, &hunters, &victum);

  CalculateSteps(&rules, &shift_points, hunters, &victum);

  WriteSteps(argv[2], &shift_points);

  free(hunters);
  free(shift_points.Points);

  return 0;
}