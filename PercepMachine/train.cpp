#include<iostream>
#include<algorithm>
#include<vector>
#include<fstream>

using namespace std;

typedef vector<double> feature;
typedef int label;

class PercepMachine
{
private:
    vector<feature> dataset;
    vector<label> labelset;
    double learningrate;
    double vector_multi (const feature &x, const feature &y)
    {
        double sum = 0.0;
        for (int i = 0; i != x.size(); ++i)
        {
            sum += x[i] * y[i];
        }
        return sum;
    }
    feature vector_multi(double x, const feature &y)
    {
        feature temp;
        for (int i = 0; i != y.size(); ++i)
        {
            temp.push_back(x*y[i]);
        }
        return temp;
    }
    feature vector_add(const feature &x, const feature &y)
    {
        feature temp(0);
        for (int i = 0; i != x.size(); ++i)
        {
            temp.push_back(x[i] + y[i]);
        }
        return temp;
    }
public:
    feature w;
    double b;
    PercepMachine(vector<feature> &traindata, vector<label> &trainlabel, feature &startw, double startb, double rate) :dataset(traindata), labelset(trainlabel), w(startw), b(startb), learningrate(rate){}
    void calculate_percep();
};

void PercepMachine::calculate_percep()
{
    vector<int> flag(dataset.size(), 1);
    while (find(flag.begin(), flag.end(), 1) != flag.end())
    {
        for (int i = 0; i != dataset.size(); ++i)
        {
            double multi = vector_multi(dataset[i], w);
            if ((multi + b)*labelset[i] <= 0)//有误分类点
            {
                flag[i] = 1;
                w = vector_add(w, vector_multi(learningrate*labelset[i], dataset[i]));
                b = b + learningrate*labelset[i];

            }
            else
            {
                flag[i] = 0;
            }
        }
    }
}

int main()
{
    ifstream  fin("data.txt");
    if (!fin)
    {
        cout << "can not open the file data.txt" << endl;
        exit(1);
    }
    /* input the dataSet 假设是平面数据，存储在txt文件中3列多行，最后一列存储类别信息1或-1*/
    int feature_dimension = 2;

    vector<feature> traindata;
    vector<label> trainlabel;
    while (!fin.eof())
    {
        feature temp_data;
        double temp;
        for (int i = 0; i < feature_dimension; ++i)
        {
            fin >> temp;
            temp_data.push_back(temp);
        }
        traindata.push_back(temp_data);
        label mylabel;
        fin >> mylabel;
        trainlabel.push_back(mylabel);
    }
    feature startw(2,1);
    double startb = 1.0;
    double rate = 0.5;

    PercepMachine permachine(traindata, trainlabel, startw, startb, rate);
    permachine.calculate_percep();
    cout << "w=" << "("<<permachine.w[0] << " " << permachine.w[1]<<")" << endl;
    cout << "b=" << permachine.b << endl;

    return 0;

}
