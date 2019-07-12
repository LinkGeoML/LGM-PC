class config:

    poi_fpath = '/media/disk/LGM-Classification-mybranch/data/marousi_pois.csv'

    experiments_path = '/media/disk/LGM-Classification-mybranch/experiments'

    supported_adjacency_features = [
        'classes_in_radius_bln', 'classes_in_radius_cnt',
        'classes_in_street_and_radius_bln', 'classes_in_street_and_radius_cnt',
        'classes_in_neighbors_bln', 'classes_in_neighbors_cnt',
        'classes_in_street_radius_bln', 'classes_in_street_radius_cnt',
    ]

    supported_textual_features = [
        'similarity_per_class', 'top_k_terms',
        'top_k_trigrams', 'top_k_fourgrams',
    ]

    supported_geometric_features = [
        # 'area', 'perimeter', 'n_vertices',
        # 'mean_edge_length', 'var_edge_length'
    ]

    included_adjacency_features = [
        'classes_in_radius_bln',
        'classes_in_radius_cnt',
        'classes_in_street_and_radius_bln',
        'classes_in_street_and_radius_cnt',
        'classes_in_neighbors_bln',
        'classes_in_neighbors_cnt',
        # 'classes_in_street_radius_bln',
        # 'classes_in_street_radius_cnt',
    ]

    included_textual_features = [
        'similarity_per_class',
        'top_k_terms',
        'top_k_trigrams',
        'top_k_fourgrams'
    ]

    included_geometric_features = [
        # 'area',
        # 'perimeter',
        # 'n_vertices',
        # 'mean_edge_length',
        # 'var_edge_length'
    ]

    normalized_features = [
        'classes_in_radius_cnt',
        'classes_in_street_and_radius_cnt',
        'classes_in_neighbors_cnt',
        'classes_in_street_radius_cnt',
        'similarity_per_class'
    ]

    classes_in_radius_thr = [200]
    classes_in_street_and_radius_thr = [300]
    classes_in_neighbors_thr = [5]
    classes_in_street_radius_thr = [100]

    top_k_terms_pct = [0.1]
    top_k_trigrams_pct = [0.1]
    top_k_fourgrams_pct = [0.1]

    # matching_strategy = [
    #     {1: ['within', ['named', 20000], ['avg_lgm_sim_dl', 0.5, None]],
    #      2: ['within', ['unnamed', 10000], [None, None, None]],
    #      3: ['nearby', ['named', 20000], ['lgm_sim_jw', 0.5, 50]],
    #      4: ['nearby', ['unnamed', 10000], [None, None, 50]]}
    # ]

    n_folds = 5

    supported_classifiers = [
        'Baseline',
        'Naive Bayes',
        'Gaussian Process',
        'AdaBoost',
        'MLP',
        'SVM',
        'Nearest Neighbors',
        'Decision Tree',
        'Random Forest',
        'Extra Trees'
    ]

    included_classifiers = [
        'Baseline',
        'Naive Bayes',
        # 'Gaussian Process',
        # 'AdaBoost',
        # 'MLP',
        'SVM',
        'Nearest Neighbors',
        # 'Decision Tree',
        'Random Forest',
        # 'Extra Trees'
    ]

    NaiveBayes_hyperparameters = {}
    GaussianProcess_hyperparameters = {}
    AdaBoost_hyperparameters = {}
    SVM_hyperparameters = [
        {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [0.01, 1, 100]},
        {'kernel': ['poly'], 'degree': [1, 2, 3], 'C': [0.01, 1, 100]},
        {'kernel': ['linear'], 'C': [0.01, 1, 100]}
    ]
    kNN_hyperparameters = {'n_neighbors': [3, 5, 10]}
    # DecisionTree_hyperparameters = {
    #     'max_depth': [i for i in range(1, 33)],
    #     'min_samples_split': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    #     'min_samples_leaf': [0.1, 0.2, 0.3, 0.4, 0.5],
    #     'max_features': [i for i in range(1, 10)]}
    DecisionTree_hyperparameters = {
        'max_depth': [1, 4, 16],
        'min_samples_split': [0.1, 0.5, 1.0]}
    # RandomForest_hyperparameters = {
    #     'bootstrap': [True, False],
    #     'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
    #     'criterion': ['gini', 'entropy'],
    #     'max_features': ['auto', 'sqrt'],
    #     'min_samples_leaf': [1, 2, 4],
    #     'min_samples_split': [2, 5, 10],
    #     'n_estimators': [250, 500, 1000]}
    RandomForest_hyperparameters = {
        'max_depth': [10, 100, None],
        'n_estimators': [250, 1000]}
    # MLP_hyperparameters = {
    #     'learning_rate_init': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1],
    #     'max_iter': [100, 200, 500, 1000],
    #     'solver': ['sgd', 'adam']}
    MLP_hyperparameters = {
        'learning_rate_init': [0.0001, 0.01, 0.1],
        'max_iter': [100, 200, 500]}

    k_preds = 5
    osm_crs = 4326

    # Marousi
    id_col = 'poi_id'
    name_col = 'name'
    label_col = 'class_name'
    lon_col = 'x'
    lat_col = 'y'
    poi_crs = 2100
    # Format: [<minlat>, <minlon>, <maxlat>, <maxlon>]
    osm_bbox = [38.0206, 23.7727, 38.0671, 23.8342]

    # # yelp Las Vegas
    # id_col = 'business_id'
    # name_col = 'name'
    # label_col = 'category'
    # lon_col = 'longitude'
    # lat_col = 'latitude'
    # poi_crs = 4326
    # # Format: [<minlat>, <minlon>, <maxlat>, <maxlon>]
    # osm_bbox = [35.9208835, -115.4529935592, 36.381974, -114.8875063285]
