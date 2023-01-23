void revertConfig(double currentLength, double* mem_preparedLength, double* mem_preparedTime);
void setConfig(double length, double time, double* mem_preparedLength, double* mem_preparedTime);
StaticJsonDocument<512> setQuadraticConfig(DynamicJsonDocument doc);
StaticJsonDocument<512> revertQuadraticConfig();
