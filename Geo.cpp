// CPP buat jyari deret geometri
#include <bits/stdc++.h>

using namespace std;
 
void printGP(int a, int r, int n)
{
  int curr_term;
  for (int i = 0; i < n; i++) {
    curr_term = a * pow(r, i);
    cout << curr_term << " ";
  }

}

// Driver code

int main()
{
  int a = 2; // angka pertama
  int r = 3; // selisih
  int n = 2; // N yg mau dicari
  printGP(a, r, n);
  return 0;
}
