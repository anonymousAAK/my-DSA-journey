/*
 * WEEK 4 — C++ Pattern Printing
 * Master nested loops with various star, number, and alphabet patterns.
 */
#include <iostream>
#include <string>
using namespace std;

void rightTriangleStars(int n) {
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j < i; j++) cout << "* ";
        cout << endl;
    }
}

void invertedTriangle(int n) {
    for (int i = n; i >= 1; i--) {
        for (int j = 0; j < i; j++) cout << "* ";
        cout << endl;
    }
}

void pyramid(int n) {
    for (int i = 1; i <= n; i++) {
        for (int s = 0; s < n - i; s++) cout << " ";
        for (int j = 0; j < i; j++) cout << "* ";
        cout << endl;
    }
}

void diamond(int n) {
    for (int i = 1; i <= n; i++) {
        cout << string(n - i, ' ');
        for (int j = 0; j < i; j++) cout << "* ";
        cout << endl;
    }
    for (int i = n - 1; i >= 1; i--) {
        cout << string(n - i, ' ');
        for (int j = 0; j < i; j++) cout << "* ";
        cout << endl;
    }
}

void numberPyramid(int n) {
    for (int i = 1; i <= n; i++) {
        cout << string(n - i, ' ');
        for (int j = 1; j <= i; j++) cout << j << " ";
        cout << endl;
    }
}

void alphabetTriangle(int n) {
    for (int i = 0; i < n; i++) {
        char ch = 'A' + i;
        for (int j = 0; j <= i; j++) cout << ch << " ";
        cout << endl;
    }
}

void floydTriangle(int n) {
    int num = 1;
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j < i; j++) {
            cout << num << " ";
            num++;
        }
        cout << endl;
    }
}

void butterfly(int n) {
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j < i; j++) cout << "* ";
        for (int j = 0; j < 2*(n-i); j++) cout << "  ";
        for (int j = 0; j < i; j++) cout << "* ";
        cout << endl;
    }
    for (int i = n; i >= 1; i--) {
        for (int j = 0; j < i; j++) cout << "* ";
        for (int j = 0; j < 2*(n-i); j++) cout << "  ";
        for (int j = 0; j < i; j++) cout << "* ";
        cout << endl;
    }
}

void hollowRectangle(int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (i == 0 || i == rows-1 || j == 0 || j == cols-1) cout << "* ";
            else cout << "  ";
        }
        cout << endl;
    }
}

int main() {
    int n = 5;

    cout << "=== Right Triangle ===" << endl;
    rightTriangleStars(n);

    cout << "\n=== Inverted Triangle ===" << endl;
    invertedTriangle(n);

    cout << "\n=== Pyramid ===" << endl;
    pyramid(n);

    cout << "\n=== Diamond ===" << endl;
    diamond(n);

    cout << "\n=== Number Pyramid ===" << endl;
    numberPyramid(n);

    cout << "\n=== Alphabet Triangle ===" << endl;
    alphabetTriangle(n);

    cout << "\n=== Floyd's Triangle ===" << endl;
    floydTriangle(n);

    cout << "\n=== Butterfly ===" << endl;
    butterfly(4);

    cout << "\n=== Hollow Rectangle 4x6 ===" << endl;
    hollowRectangle(4, 6);

    return 0;
}
