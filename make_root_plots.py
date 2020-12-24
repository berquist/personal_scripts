
import matplotlib as mpl
mpl.use('Agg')
# mpl.rc('text', usetex=True)
import matplotlib.pyplot as plt

from gtot import results


labels = ('4w0a', '3w1a', '2w2a_trans', '2w2a_cis', '1w3a', '0w4a')
labels_pretty = ('4w0a', '3w1a', '2w2a (trans)', '2w2a (cis)', '1w3a', '0w4a')
label_map = {labels[i]:labels_pretty[i] for i in range(len(labels))}
xvals = range(len(labels))
active_spaces = ('9_5_5', '17_9_9')
active_spaces_pretty = ('(9,5)', '(17,9)')
active_space_map = {active_spaces[i]:active_spaces_pretty[i] for i in range(len(active_spaces))}

# Inject some dictionaries into the namespace!
for active_space in active_spaces:
    define_active_space_dict = """results_{0} = dict()""".format(active_space)
    exec(define_active_space_dict)

# Inject some more dictionaries into the namespace!
for key in results:

    system = labels[[label in key for label in labels].index(True)]
    active_space = active_spaces[[active_space in key for active_space in active_spaces].index(True)]
    active_space_dict_str = 'results_{}'.format(active_space)
    nroots = int(active_space.split('_')[-1])
    root_weights_str = key.split('.')[-2]
    root_weights = [float('0.' + weight[1:]) for weight in root_weights_str.split('_')]
    root_weights_dict_str = "{active_space_dict}['{system}']['{root_weights}']".format(active_space_dict=active_space_dict_str,
                                                                                       system=system,
                                                                                       root_weights=root_weights_str)

    define_system_dict = """if not '{system}' in {active_space_dict}:
    {active_space_dict}['{system}'] = dict()
""".format(system=system, active_space_dict=active_space_dict_str)
    define_root_weights_dict = """if not '{root_weights}' in {active_space_dict}['{system}']:
    {active_space_dict}['{system}']['{root_weights}'] = dict()
""".format(root_weights=root_weights_str, active_space_dict=active_space_dict_str, system=system)

    exec(define_system_dict)
    exec(define_root_weights_dict)
    exec(root_weights_dict_str + "['weights'] = " + str(root_weights))
    exec(root_weights_dict_str + ".update(results['{}'])".format(key))

# Inject some lists into the namespace!
results_list_names = []
for active_space in active_spaces:
    for system in labels:
        results_list_name_str = "results_{}_{}".format(active_space, system)
        results_list_comprehension_str = "[(v['weights'], v['g1'], v['g2'], v['g3'], v['giso']) for v in results_{}['{}'].values()]".format(active_space, system)
        try:
            exec(' '.join([results_list_name_str, '=', results_list_comprehension_str]))
            results_list_names.append(results_list_name_str)
        except KeyError:
            print('oops! results not present for {}'.format(results_list_name_str))

# 1. Weight of 1st root increases, all others decrease equally
# 2. Weight of 1st root increases, 2nd stays constant, all others decrease equally
# 3. Weights of 1st and 2nd root increase equally, all others decrease equally
# sort all values by weight of the lowest root
sortkey = lambda v: v[0][0]
for results_list_name in results_list_names:
    results_list_name_1_str = "{}_1".format(results_list_name)
    results_list_name_2_str = "{}_2".format(results_list_name)
    results_list_name_3_str = "{}_3".format(results_list_name)
    results_list_comprehension_1_str = "sorted([v for v in {} if v[0][1] == v[0][2]], key=sortkey)".format(results_list_name)
    results_list_comprehension_2_str = "sorted([v for v in {} if v[0][1] != v[0][2]], key=sortkey)".format(results_list_name)
    results_list_comprehension_3_str = "sorted([v for v in {} if v[0][0] == v[0][1]], key=sortkey)".format(results_list_name)
    exec(' '.join([results_list_name_1_str, '=', results_list_comprehension_1_str]))
    exec(' '.join([results_list_name_2_str, '=', results_list_comprehension_2_str]))
    exec(' '.join([results_list_name_3_str, '=', results_list_comprehension_3_str]))

### Common plot settings.

kwargs_legend = {
    'loc': 'best',
    'fancybox': True,
    'framealpha': 0.5,
}

fontsize_xticks = 14
fontsize_xlabel = 16
fontsize_yticks = 16
fontsize_ylabel = 20

y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)

for weighting_scheme in (1, 2, 3):
    for active_space in active_spaces:
        for system in labels:

            exec_plot_str = """
ax.plot([(v[0][0]) for v in results_{active_space}_{system}_{scheme}],
        [v[3] for v in results_{active_space}_{system}_{scheme}], marker='o', label='root 1')
ax.plot([sum(v[0][0:2]) for v in results_{active_space}_{system}_{scheme}],
        [v[3] for v in results_{active_space}_{system}_{scheme}], marker='o', label='root 1 + 2')
ax.plot([sum(v[0][0:3]) for v in results_{active_space}_{system}_{scheme}],
        [v[3] for v in results_{active_space}_{system}_{scheme}], marker='o', label='root 1 + 2 + 3')
ax.plot([sum(v[0][0:4]) for v in results_{active_space}_{system}_{scheme}],
        [v[3] for v in results_{active_space}_{system}_{scheme}], marker='o', label='root 1 + 2 + 3 + 4')
""".format(active_space=active_space, system=system, scheme=weighting_scheme)

            fig, ax = plt.subplots()

            try:
                exec(exec_plot_str)
                ax.legend(**kwargs_legend)
                ax.set_title('system: {} active space: {}'.format(label_map[system], active_space_map[active_space]))
                ax.set_xlabel('weight')
                ax.set_xlim((0.0, 1.0))
                ax.set_ylabel(r'$g_{\parallel}$')
                ax.yaxis.set_major_formatter(y_formatter)
                fig.savefig('fig0{}_{}_{}.pdf'.format(weighting_scheme, active_space, system), bbox_inches='tight')
            # There's a chance the parent variable hasn't been defined yet.
            except NameError:
                print("oops! can't make plot for {}_{}".format(active_space, system))
