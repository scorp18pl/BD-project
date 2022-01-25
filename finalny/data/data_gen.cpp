#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <random>

using Attribute = std::pair<std::string, std::string>;

class RandomNumberGen {
public:
	template <typename VType>
	static VType getRandom(VType min, VType max);
};

template <typename VType>
VType RandomNumberGen::getRandom(VType min, VType max) {
	return VType();
}


template <>
int RandomNumberGen::getRandom(int min, int max) {
	static std::random_device dev;
	static std::mt19937 rng(dev());
	std::uniform_int_distribution<> dist(min, max - 1);

	return dist(rng);
}

template <>
float RandomNumberGen::getRandom(float min, float max) {
	static std::random_device dev;
	static std::mt19937 rng(dev());
	std::uniform_real_distribution<> dist(min, max);

	return dist(rng);
}


class IdGen {
public:
	int assignId();
	int getNextId();
	int getRandomId();
private:
	int id = 0;
};

int IdGen::assignId() {
	return id++;
}

int IdGen::getNextId() {
	return id - 1;
}

int IdGen::getRandomId() {
	return RandomNumberGen::getRandom<int>(0, id);
}

template <typename VType>
class VGen {
public:
	VGen(VType min, VType max);

	std::string getValue();
private:
	int min, max;
};

template <typename VType>
VGen<VType>::VGen(VType min, VType max)
	: min(min), max(max) {
}

template <typename VType>
std::string VGen<VType>::getValue() {
	return std::to_string(RandomNumberGen::getRandom<VType>(min, max));
}

class VGenString {
	std::vector<std::string> names;

public:
	VGenString(std::string filepath);

	std::string getValue();
};


VGenString::VGenString(std::string filepath) {
	std::ifstream file(filepath);

	std::string name;
	while (file >> name) {
		names.push_back("'" + name + "'");
	}
}

std::string VGenString::getValue() {
	return names[RandomNumberGen::getRandom<int>(0, names.size())];
}

class Global {
public:
	static VGenString name_gen;
	static std::ofstream output_file;

	static IdGen atmosphere_id_gen_pref;
	static IdGen Race_id_gen;

	static IdGen atmosphere_id_gen;
	static IdGen composition_id_gen;

	static IdGen galaxy_id_gen;
	static IdGen system_id_gen;
	static IdGen star_id_gen;
	static IdGen planet_id_gen;
};

IdGen Global::atmosphere_id_gen_pref = IdGen();
IdGen Global::Race_id_gen = IdGen();

IdGen Global::atmosphere_id_gen = IdGen();
IdGen Global::composition_id_gen = IdGen();

IdGen Global::galaxy_id_gen = IdGen();
IdGen Global::system_id_gen = IdGen();
IdGen Global::star_id_gen = IdGen();
IdGen Global::planet_id_gen = IdGen();

VGenString Global::name_gen = VGenString("names.txt");
std::ofstream Global::output_file;

class Table {
public:
	void print();

	Table() = default;
	Table(std::string name, std::vector<Attribute> &&atts);
private:
	std::string name;
	std::vector<Attribute> attributes;
};

Table::Table(std::string name, std::vector<Attribute> &&atts) 
	: name(name), attributes(atts){
}

void Table::print() {
	Global::output_file << "INSERT INTO " << name << "(";
	for (unsigned i = 0; i < attributes.size(); ++i) {
		Global::output_file << attributes[i].first;
		
		if (i < attributes.size() - 1) {
			Global::output_file << ",";
		}
		else {
			Global::output_file << ")";
		}
	}

	Global::output_file << " VALUES (";
	for (unsigned i = 0; i < attributes.size(); ++i) {
		Global::output_file << attributes[i].second;

		if (i < attributes.size() - 1) {
			Global::output_file << ",";
		}
	}
	Global::output_file << ");\n";
}

class Composition {
public:
	Composition(int at_id,float concentration);
	void print();

private:
	int id;
	Table t;
};

Composition::Composition(int at_id, float concentration)
	: id(Global::composition_id_gen.assignId()) {
	static const int ELEMENT_COUNT = 118;
	static VGen<int> el_gen(1, ELEMENT_COUNT + 1);

	std::vector<Attribute> atts;
	atts.push_back(Attribute("id", std::to_string(id)));
	atts.push_back(Attribute("atmosphere", std::to_string(at_id)));
	atts.push_back(Attribute("concentration", std::to_string(concentration)));
	atts.push_back(Attribute("element", el_gen.getValue()));
	t = Table("Composition", std::move(atts));
}

void Composition::print() {
	t.print();
}

class Atmosphere {
public:
	Atmosphere();
	void print();
private:
	int id;
	int comp_count;

	Table t;
};

Atmosphere::Atmosphere() 
	: id(Global::atmosphere_id_gen.assignId()), 
	comp_count(RandomNumberGen::getRandom<int>(1, 8)) {
	static VGen<float> pressure_gen(0.001f, 1000000.0f);

	std::vector<Attribute> atts;
	atts.push_back(Attribute("id", std::to_string(id)));
	atts.push_back(Attribute("pressure", pressure_gen.getValue()));
	t = Table("Atmosphere", std::move(atts));
}

void Atmosphere::print() {
	t.print();

	float remainder = 1.0f;
	for (int i = 0; i < comp_count - 1; ++i) {
		float fraction = RandomNumberGen::getRandom<float>(0.0f, 0.8f);
		
		float concentration = remainder * fraction;
		remainder -= concentration;

		Composition c(id, concentration);
		c.print();
	}
	// Complement
	{
		Composition c(id, remainder * 0.9f);
		c.print();
	}
}

class Race {
public:
	Race(int atmosphere_id);
	void print();
private:
	int id;
	Table t;
};

Race::Race(int atmosphere_id) 
	: id(Global::Race_id_gen.assignId()){
	static VGen<int> temp_gen(0, 10000);
	static VGen<float> grav_gen(0.0f, 100.00f);
	static VGen<float> hermit_gen(0.0f, 1.0f);
	static VGen<float> peace_gen(0.0f, 1.0f);

	std::vector<Attribute> atts;
	atts.push_back(Attribute("id", std::to_string(id)));
	atts.push_back(Attribute("identif", Global::name_gen.getValue()));

	atts.push_back(Attribute("temperature", temp_gen.getValue()));
	atts.push_back(Attribute("grav_acc", grav_gen.getValue()));
	atts.push_back(Attribute("hermit_level", hermit_gen.getValue()));
	atts.push_back(Attribute("peacefulness", peace_gen.getValue()));

	bool is_rocky = RandomNumberGen::getRandom<float>(0.0f, 1.0f) > 0.8f;
	atts.push_back(Attribute("planet_type", is_rocky ? "'rocky'" : "'gaseous'"));
	atts.push_back(Attribute("atmosphere", std::to_string(atmosphere_id)));

	t = Table("Race", std::move(atts));
}

void Race::print() {
	t.print();
}

class Planet {
public:
	Planet(int star);
	void print();
private:
	int id;
	Table t;
};

Planet::Planet(int star) 
	:id(Global::planet_id_gen.assignId()) {

	static VGen<float> mass_gen(0.0001f, 100.0f);
	static VGen<float> radius_gen(0.0001f, 100.0f);
	static VGen<float> star_dist_gen(0.001f, 1000.0f);
	static VGen<float> aggression_gen(0.0f, 1.0f);

	std::vector<Attribute> atts;
	atts.push_back(Attribute("id", std::to_string(id)));
	atts.push_back(Attribute("identif", Global::name_gen.getValue()));

	bool is_rocky = RandomNumberGen::getRandom<float>(0.0f, 1.0f) > 0.8f;
	atts.push_back(Attribute("planet_type", is_rocky ? "'rocky'" : "'gaseous'"));

	atts.push_back(Attribute("mass", mass_gen.getValue()));
	atts.push_back(Attribute("radius", radius_gen.getValue()));
	atts.push_back(Attribute("atmosphere", 
							 std::to_string(Global::atmosphere_id_gen.getRandomId())));
	atts.push_back(Attribute("star", std::to_string(star)));
	atts.push_back(Attribute("star_distance", star_dist_gen.getValue()));

	bool inhibited = RandomNumberGen::getRandom<float>(0.0f, 1.0f) > 0.8f;
	atts.push_back(Attribute("alien_aggression_level", inhibited ? aggression_gen.getValue() : "NULL"));

	t = Table("Planet", std::move(atts));
}

void Planet::print() {
	t.print();
}

class Star {
public:
	Star(int system_id);

	void print();
private:
	int id;
	Table t;
};

void Star::print() {
	t.print();
}

Star::Star(int system_id)
	:id(Global::star_id_gen.assignId()) {
	static VGen<float> lum_gen(0.01f, 10000000.0f);
	static VGen<float> mass_gen(0.01f, 1000.0f);

	std::vector<Attribute> atts;
	atts.push_back(Attribute("id", std::to_string(id)));
	atts.push_back(Attribute("identif", Global::name_gen.getValue()));
	atts.push_back(Attribute("luminosity", lum_gen.getValue()));
	atts.push_back(Attribute("mass", mass_gen.getValue()));
	atts.push_back(Attribute("solar_system", std::to_string(system_id)));

	t = Table("Star", std::move(atts));
}

class System {
public:
	System(int galaxy_id);

	void print();
private:
	int id;

	Table t;
	int planet_count;
	int star_count;

	static const int MAX_PLANET_COUNT = 20;
	static const int MAX_STAR_COUNT = 6;
};

System::System(int galaxy_id) 
	:id(Global::system_id_gen.assignId()) {
	static VGen<float> stab_gen(0.0f, 1.0f);

	std::vector<Attribute> atts;
	atts.push_back(Attribute("id", std::to_string(id)));
	atts.push_back(Attribute("identif", Global::name_gen.getValue()));
	atts.push_back(Attribute("stability", stab_gen.getValue()));
	atts.push_back(Attribute("galaxy", std::to_string(galaxy_id)));

	t = Table("SolarSystem", std::move(atts));

	planet_count = RandomNumberGen::getRandom<int>(1, MAX_PLANET_COUNT);
	star_count = RandomNumberGen::getRandom<int>(1, MAX_STAR_COUNT);
}

void System::print() {
	t.print();

	int first_star_id = Global::star_id_gen.getNextId();
	for (int i = 0; i < star_count; ++i) {
		Star s(id);
		s.print();
	}
	int next_star_id = Global::star_id_gen.getNextId();

	for (int i = 0; i < planet_count; ++i) {
		Planet p(RandomNumberGen::getRandom<int>(first_star_id, next_star_id));
		p.print();
	}
}

class Galaxy {
public:
	Galaxy();

	void print();
private:
	int id;
	Table t;
};

Galaxy::Galaxy() 
	:id(Global::galaxy_id_gen.assignId()) {
	static VGen<int> dist_gen = VGen<int>(0, 100000000);

	std::vector<Attribute> atts;
	atts.push_back(Attribute("id", std::to_string(id)));
	atts.push_back(Attribute("identif", Global::name_gen.getValue()));
	atts.push_back(Attribute("distance", dist_gen.getValue()));

	t = Table("Galaxy", std::move(atts));
}

void Galaxy::print() {
	static const int SYSTEM_COUNT = 100;

	t.print();
	for (int i = 0; i < SYSTEM_COUNT; ++i) {
		System s(id);
		s.print();
	}
}

class DataGen {
public:
	void start();
};

void DataGen::start() {
	static const int ATMOSPHERE_COUNT = 10;
	for (int i = 0; i < ATMOSPHERE_COUNT; ++i) {
		Atmosphere a;
		a.print();
	}

	static const int GALAXY_COUNT = 10;
	for (int i = 0; i < GALAXY_COUNT; ++i) {
		Galaxy g;
		g.print();
	}

	static const int PREF_COUNT = 10;
	for (int i = 0; i < PREF_COUNT; ++i) {
		Atmosphere a;
		a.print();

		Race p(ATMOSPHERE_COUNT + i);
		p.print();
	}
}

int main() {
	Global::output_file.open("insert_rest.sql");

	DataGen dg;
	dg.start();

	Global::output_file.close();

	return 0;
}
