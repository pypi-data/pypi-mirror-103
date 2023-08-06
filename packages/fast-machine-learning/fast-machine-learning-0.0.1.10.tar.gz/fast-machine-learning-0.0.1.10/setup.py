from setuptools import setup, find_packages

setup(
    name='fast-machine-learning',
    version='0.0.1.10',
    description=(
        'Enhance and remake my first pkg luktianutl (partially in current) which is still under remaking. '
    ),
    author='luktian',
    author_email='luktian@shu.edu.cn',
    maintainer='luktian',
    maintainer_email='luktian@shu.edu.cn',
    license='BSD License',
    packages=find_packages(exclude=[
        "tests", "*.tests", "*.tests.*", "tests.*", "__pycache__", "fml001.pyproj", 
        "fml001.pyproj.user", "joblibfile", "*.xlsx", "generator_sp.py",
        ]),
    data_files=[
        ('lib/site-packages/fml/feature_selection/exec',['fml/feature_selection/exec/mrmr']),
        ('lib/site-packages/fml/feature_selection/exec',['fml/feature_selection/exec/mrmr.exe']),
        ('lib/site-packages/fml/descriptors',['fml/descriptors/c9tc06632b3.joblib']),
        ('lib/site-packages/fml/descriptors',['fml/descriptors/c9tc06632b4.joblib']),
        ('lib/site-packages/fml/descriptors',['fml/descriptors/v.joblib']),
        ('lib/site-packages/fml/descriptors',['fml/descriptors/m.joblib']),
        ('lib/site-packages/fml/descriptors',['fml/descriptors/m_ionic_energies.joblib']),
        ('lib/site-packages/fml/descriptors',['fml/descriptors/m_ionic_oxidation_states.joblib']),
        ('lib/site-packages/fml/descriptors',['fml/descriptors/m_ionic_radii.joblib']),
        ('lib/site-packages/fml/descriptors',['fml/descriptors/m_meaning.joblib']),
        ('lib/site-packages/fml/descriptors',['fml/descriptors/organic_descriptors.joblib']),
        ('lib/site-packages/fml/descriptors',['fml/descriptors/organic_list.joblib']),
        ],
    platforms=["windows"],
    python_requires=">=3.6",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'sklearn',
        'numpy',
        'scipy',
        'shap',
        'deap',
        'hyperopt'
    ],
)