// Test-only runner for Max-exported Gen C++. No generated/vendor code is tracked.
// Compile with GEN_HEADER="voice.h" and GEN_NAMESPACE=voice.
#include GEN_HEADER
#include <chrono>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
namespace dsp = GEN_NAMESPACE;

int main(int argc, char** argv) {
    if (argc < 4) return 2;
    const double sr = std::stod(argv[1]), seconds = std::stod(argv[2]);
    const int block = 64, channels = dsp::num_outputs();
    auto* state = static_cast<CommonState*>(dsp::create(sr, block));
    auto set = [&](const std::string& key, double value) {
        for (int i=0;i<dsp::num_params();++i) {
            if (key == dsp::getparametername(state,i)) {
                dsp::setparameter(state,i,value,nullptr); return true;
            }
        }
        std::cerr << "Unknown Gen parameter: " << key << '\n'; return false;
    };
    double release = -1, sweep = -1, initialRpm = 740;
    bool inputTest = false;
    for (int i=4;i<argc;++i) {
        std::string arg(argv[i]); auto split = arg.find('=');
        if (split==std::string::npos) return 2;
        auto key=arg.substr(0,split); double value=std::stod(arg.substr(split+1));
        if (key=="release_seconds") release=value;
        else if (key=="sweep_end") sweep=value;
        else if (key=="test_mix_input") inputTest=value!=0;
        else if (!set(key,value)) return 3;
        if (key=="rpm") initialRpm=value;
    }
    std::vector<std::vector<t_sample>> inputs(std::max(4,dsp::num_inputs()),std::vector<t_sample>(block));
    std::vector<std::vector<t_sample>> outputs(channels,std::vector<t_sample>(block));
    std::vector<t_sample*> in, out;
    for(auto& v:inputs) in.push_back(v.data());
    for(auto& v:outputs) out.push_back(v.data());
    const long frames=static_cast<long>(seconds*sr);
    std::ofstream file(argv[3],std::ios::binary);
    if (!file) return 4;
    double micros=0, peak=0;
    bool released=false;
    for (long frame=0;frame<frames;frame+=block) {
        const int n=std::min<long>(block,frames-frame);
        if(release>=0 && frame>=release*sr && !released) {set("throttle",0);set("load",0);released=true;}
        if(sweep>=0) set("rpm",initialRpm+(sweep-initialRpm)*frame/frames);
        if(inputTest) for(int i=0;i<n;i++) {
            double time=(frame+i)/sr;
            inputs[0][i]=.10*std::cos(time*6.283185307179586*70)+.08*std::cos(time*6.283185307179586*750);
            inputs[3][i]=1;
        }
        auto begin=std::chrono::steady_clock::now();
        int error=dsp::perform(state,in.data(),dsp::num_inputs(),out.data(),channels,n);
        micros+=std::chrono::duration<double,std::micro>(std::chrono::steady_clock::now()-begin).count();
        if(error) return 5;
        for(int i=0;i<n;i++) for(int channel=0;channel<channels;channel++) {
            double sample=outputs[channel][i];
            if(!std::isfinite(sample)) return 6;
            peak=std::max(peak,std::abs(sample));
            file.write(reinterpret_cast<const char*>(&sample),sizeof(sample));
        }
    }
    dsp::destroy(state);
    std::cout<<"{\"sample_rate\":"<<sr<<",\"frames\":"<<frames<<",\"channels\":"<<channels
             <<",\"peak\":"<<peak<<",\"dsp_microseconds\":"<<micros<<"}\n";
}
