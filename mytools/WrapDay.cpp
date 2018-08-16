#include <iostream>
#include <cstring>
#include <regex>
#include <fstream>

int main(int argv, char*argc[])
{
    std::string ifilename, ofilename, lineTemp;
    const std::string pattern = "(<tr>)(<td([^>]*)?>日期: [0-9]{4}-[0-9]{2}-[0-9]{2}</td></tr>)",
        BeginSign = "(</div><div class='wrap_day'><table width=100% cellspacing=0><tr><td(.*)?>日期:)";

    std::regex SplitSign(pattern, std::regex_constants::optimize),
        begSign(BeginSign, std::regex_constants::optimize);
    std::smatch ThisMatch;

    if(argv > 2) ifilename = argc[1], ofilename = argc[2];
    else std::cin >> ifilename >>ofilename;

    std::fstream infile(ifilename, std::ios_base::in);
    if(infile.is_open())
    {
        std::fstream outfile(ofilename, std::ios_base::out);
        if(outfile.is_open())
        {
            std::string file = "";
            while (std::getline(infile, lineTemp))
            {
                if (lineTemp.find("<div class='wrap_day'>") != std::string::npos)
                {
                    std::cerr << "this file has been wrapped once" << '\n';
                    infile.close();
                    outfile.close();
                    return 1;
                }else
                {
                    if (std::regex_search(lineTemp, ThisMatch, SplitSign))
                        lineTemp.replace(ThisMatch.position(), ThisMatch.length(),
                        "</table></div><div class='wrap_day'><table width=100% cellspacing=0>" + ThisMatch.str());
                    file += lineTemp + '\n';
                    lineTemp = "";
                }
            }

            if(std::regex_search(file, ThisMatch, begSign))
                file.erase(ThisMatch.position(), strlen("</div>"));

            auto last = file.rfind("</table>");
            if (last != std::string::npos)
                file.insert(last + strlen("</table>"), "</div>");

            outfile << file;
            std::cout << ifilename << " have wrapped day into " << ofilename << std::endl;

            outfile.close();
        }
        else std::cerr << "Warning: Can't open file " << ofilename << std::endl;
        infile.close();
    }
    else std::cerr << "Warning: Can't open file " << ifilename << std::endl;

    return 0;
}
