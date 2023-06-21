void a()
{
}

int b(int i)
{
  return i + 1;
}

void c()
{
  a();
}

void main()
{
  int i;
  int j;
  a();
  j = b(i);
  c();
}

void _start()
{
  main();
}
