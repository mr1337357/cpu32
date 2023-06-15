int subtract(int a, int b)
{
  return a - b;
}

int main(int argc,char **argv)
{
  char *message = "asdf";
  int a = 525600;
  int b = 365;
  int c = subtract(a,b);
  //int d = a/b;
  message[1] = 'g';
  return 0;
}

void _start()
{
  main(0,0);
}
