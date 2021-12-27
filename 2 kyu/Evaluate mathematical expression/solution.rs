extern crate bit_set;

use std::convert::AsRef;
use std::cmp;
use std::mem;
use std::collections::{BTreeSet, BTreeMap};
use std::iter;

use bit_set::BitSet;

#[derive(Clone, Copy, Debug, Eq, PartialEq, Ord, PartialOrd)]
struct Symbol(u32);

struct Grammar {
    rules: Vec<Rule>,
    start_symbol: Option<Symbol>,
    symbol_source: SymbolSource,
}

struct BinarizedGrammar {
    rules: Vec<BinarizedRule>,
    start_symbol: Option<Symbol>,
    symbol_source: SymbolSource,
}

struct Rule {
    lhs: Symbol,
    rhs: Vec<Symbol>,
    id: usize,
}

#[derive(Clone)]
struct BinarizedRule {
    lhs: Symbol,
    rhs0: Symbol,
    rhs1: Option<Symbol>,
    source: Option<usize>,
}

#[derive(Clone)]
struct SymbolSource {
    next_symbol: Symbol,
    symbol_names: Vec<String>,
}

struct RuleBuilder<'a> {
    lhs: Symbol,
    rhs: Option<Vec<Symbol>>,
    id: Option<usize>,
    grammar: &'a mut Grammar,
}

struct Tables {
    prediction_matrix: Vec<BitSet>,
    start_symbol: Symbol,
    num_syms: usize,
    rules: Vec<BinarizedRule>,
    unary_completions: Vec<Vec<PredictionTransition>>,
    binary_completions: Vec<Vec<PredictionTransition>>,
    symbol_names: Vec<String>,
}

#[derive(Copy, Clone, Debug)]
struct PredictionTransition {
    symbol: Symbol,
    dot: usize,
}

// Forest

struct Forest {
    graph: Vec<Node>,
    // summands: u32,
    summands: Vec<Product>,
    eval: Vec<Option<usize>>,
}

#[derive(Copy, Clone)]
struct Product {
    action: u32,
    left_factor: NodeHandle,
    right_factor: Option<NodeHandle>,
}

#[derive(Clone)]
enum Node {
    Sum {
        summands: Vec<Product>,
    },
    Leaf {
        terminal: Symbol,
        values: u32,
    }
}

const NULL_ACTION: u32 = !0;

// Recognizer

struct Recognizer {
    tables: Tables,
    earley_chart: Vec<EarleySet>,
    next_set: EarleySet,
    complete: BinaryHeap<CompletedItem>,
    forest: Forest,
    finished_node: Option<NodeHandle>,
}

struct EarleySet {
    predicted: BitSet,
    medial: Vec<Item>,
}

struct BinaryHeap<T> {
    vec: Vec<T>,
}

struct Item {
    dot: usize,
    origin: usize,
    node: NodeHandle,
}

#[derive(Clone, Copy)]
struct CompletedItem {
    dot: usize,
    origin: usize,
    left_node: NodeHandle,
    right_node: Option<NodeHandle>,
}

#[derive(Eq, PartialEq, Ord, PartialOrd)]
enum MaybePostdot {
    Binary(Symbol),
    Unary,
}

#[derive(Clone, Copy, Debug)]
struct NodeHandle(usize);

impl PartialEq for CompletedItem {
    fn eq(&self, other: &Self) -> bool {
        (self.origin, self.dot) == (other.origin, other.dot)
    }
}

impl Eq for CompletedItem {}

impl PartialOrd for CompletedItem {
    fn partial_cmp(&self, other: &Self) -> Option<::std::cmp::Ordering> {
        Some((self.origin, self.dot).cmp(&(other.origin, other.dot)))
    }
}

impl Ord for CompletedItem {
    fn cmp(&self, other: &Self) -> ::std::cmp::Ordering {
        (self.origin, self.dot).cmp(&(other.origin, other.dot))
    }
}

impl Symbol {
    fn usize(self) -> usize {
        self.0 as usize
    }
}

impl SymbolSource {
    fn new() -> Self {
        Self { next_symbol: Symbol(0), symbol_names: vec![] }
    }

    fn make_symbol(&mut self, name: &str) -> Symbol {
        let result = self.next_symbol;
        self.next_symbol.0 += 1;
        self.symbol_names.push(name.to_owned());
        result
    }

    fn make_n_symbols<F>(&mut self, count: usize, mut f: F) -> Vec<Symbol> where F: FnMut() -> String {
        (0..count).map(|_| self.make_symbol(&f()[..])).collect()
    }
}

impl EarleySet {
    fn new(num_syms: usize) -> Self {
        EarleySet {
            predicted: BitSet::with_capacity(num_syms),
            medial: vec![],
        }
    }
}

impl Grammar {
    fn new() -> Self {
        Self {
            rules: vec![],
            start_symbol: None,
            symbol_source: SymbolSource::new(),
        }
    }

    fn make_symbol(&mut self, name: &str) -> Symbol {
        self.symbol_source.make_symbol(name)
    }

    fn rule(&mut self, lhs: Symbol) -> RuleBuilder {
        RuleBuilder { grammar: self, lhs, rhs: None, id: None }
    }

    fn start_symbol(&mut self, symbol: Symbol) {
        self.start_symbol = Some(symbol);
    }

    fn binarize(&self) -> BinarizedGrammar {
        let mut gensym_n = 0;
        let mut symbol_source = self.symbol_source.clone();
        let binarized_rules = self.rules.iter().flat_map(|rule| {
            // Rewrite to a set of binarized rules.
            // From `LHS ⸬= A B C … X Y Z` to:
            // ____________________
            // | LHS ⸬= S0  Z
            // | S0  ⸬= S1  Y
            // | S1  ⸬= S2  X
            // | …
            // | Sm  ⸬= Sn  C
            // | Sn  ⸬= A   B
            let mut rules = vec![];

            match rule.rhs.len() {
                0 => unreachable!(),
                1 => {
                    rules.push(BinarizedRule {
                        lhs: rule.lhs,
                        rhs0: rule.rhs[0],
                        rhs1: None,
                        source: Some(rule.id),
                    });
                }
                rhs_count => {
                    let num_additional_symbols = rhs_count - 2;
                    let gensyms = symbol_source.make_n_symbols(num_additional_symbols, || {
                        let sym_name = format!("g{}", gensym_n);
                        gensym_n += 1;
                        sym_name
                    });
                    let lhs_iter = gensyms.iter().cloned().chain(iter::once(rule.lhs));
                    let mut rhs1_iter = rule.rhs.iter().cloned();
                    let rhs0_iter = rhs1_iter.next().into_iter().chain(gensyms.iter().cloned());

                    rules.extend(
                        lhs_iter.zip(rhs0_iter).zip(rhs1_iter).map(|((lhs, rhs0), rhs1)| {
                            BinarizedRule {
                                lhs,
                                rhs0,
                                rhs1: Some(rhs1),
                                source: if lhs == rule.lhs { Some(rule.id) } else { None },
                            }
                        })
                    );
                }
            }
            rules.into_iter()
        }).collect();
        BinarizedGrammar {
            rules: binarized_rules,
            symbol_source,
            start_symbol: self.start_symbol,
        }
    }
}

impl BinarizedGrammar {
    fn sort_rules(&mut self) {
        self.rules.sort_by(|a, b| a.lhs.cmp(&b.lhs));
    }
}

impl<'a> RuleBuilder<'a> {
    fn rhs<R>(mut self, rhs: R) -> Self where R: AsRef<[Symbol]> {
        assert!(rhs.as_ref().len() > 0, "empty rules are not accepted");
        self.rhs = Some(rhs.as_ref().to_vec());
        self
    }

    fn id(mut self, id: usize) -> Self {
        self.id = Some(id);
        self
    }

    fn build(self) {
        self.grammar.rules.push(
            Rule {
                lhs: self.lhs,
                rhs: self.rhs.unwrap(),
                id: self.id.unwrap_or(self.grammar.rules.len()),
            }
        );
    }
}

// Implementation for the recognizer.
//
// The recognizer has a chart of earley sets (Vec<EarleySet>) as well as the last set (next_set).
//
// A typical loop that utilizes the recognizer:
// 
// - for character in string { 
// 1.   recognizer.begin_earleme();
// 2.   recognizer.scan(token_to_symbol(character), values());
//        2a. complete
// 3.   recognizer.end_earleme();
//        3a. self.complete_all_sums_entirely();
//        3b. self.sort_medial_items();
//        3c. self.prediction_pass();
// - }
//
impl Recognizer {
    fn new(mut grammar: BinarizedGrammar) -> Self {
        grammar.sort_rules();
        let mut result = Self {
            tables: Tables::new(&grammar),
            earley_chart: vec![],
            next_set: EarleySet::new(grammar.symbol_source.next_symbol.usize()),
            forest: Forest::new(&grammar),
            // complete: BinaryHeap::new_by_key(Box::new(|completed_item| (completed_item.origin, completed_item.dot))),
            complete: BinaryHeap::with_capacity(64),
            finished_node: None,
        };
        result.initialize();
        result
    }

    fn initialize(&mut self) {
        // self.earley_chart.push(EarleySet {
        //     predicted: self.tables.prediction_matrix[self.tables.start_symbol.usize()].clone(),
        //     medial: vec![],
        // });
        let es = EarleySet {
            predicted: self.tables.prediction_matrix[self.tables.start_symbol.usize()].clone(),
            medial: vec![],
        };
        // self.earley_chart.push(mem::replace(&mut self.next_set, EarleySet::new(self.tables.num_syms)));
        self.earley_chart.push(es);
    }

    fn begin_earleme(&mut self) {
        // nothing to do
    }

    fn scan(&mut self, terminal: Symbol, values: u32) {
        let node = self.forest.leaf(terminal, self.earleme() + 1, values);
        self.complete(self.earleme(), terminal, node);
    }

    fn end_earleme(&mut self) -> bool {
        if self.is_exhausted() {
            false
        } else {
            // Completion pass, which saves successful parses.
            self.finished_node = None;
            self.complete_all_sums_entirely();
            // Do the rest.
            self.sort_medial_items();
            self.prediction_pass();
            self.earley_chart.push(mem::replace(&mut self.next_set, EarleySet::new(self.tables.num_syms)));
            true
        }
    }

    fn is_exhausted(&self) -> bool {
        self.next_set.medial.len() == 0 && self.complete.is_empty()
    }

    fn complete_all_sums_entirely(&mut self) {
        while let Some(&ei) = self.complete.peek() {
            let lhs_sym = self.tables.get_lhs(ei.dot);
            while let Some(&ei2) = self.complete.peek() {
                if ei.origin == ei2.origin && lhs_sym == self.tables.get_lhs(ei2.dot) {
                    self.forest.push_summand(ei2);
                    self.complete.pop();
                } else {
                    break;
                }
            }
            let node = self.forest.sum(lhs_sym, ei.origin);
            if ei.origin == 0 && lhs_sym == self.tables.start_symbol {
                self.finished_node = Some(node);
            }
            self.complete(ei.origin, lhs_sym, node);
        }
    }

    /// Sorts medial items with deduplication.
    fn sort_medial_items(&mut self) {
        let tables = &self.tables;
        // Build index by postdot
        // These medial positions themselves are sorted by postdot symbol.
        self.next_set.medial.sort_unstable_by(|a, b| {
            (tables.get_rhs1_cmp(a.dot), a.dot, a.origin).cmp(&(
                tables.get_rhs1_cmp(b.dot),
                b.dot,
                b.origin,
            ))
        });
    }

    fn prediction_pass(&mut self) {
        // Iterate through medial items in the current set.
        let iter = self.next_set.medial.iter();
        // For each medial item in the current set, predict its postdot symbol.
        let destination = &mut self.next_set.predicted;
        for ei in iter {
            let postdot = if let Some(rhs1) = self.tables.get_rhs1(ei.dot) {
                rhs1
            } else {
                continue;
            };
            if !destination.contains(postdot.usize()) {
                // Prediction happens here. We would prefer to call `self.predict`, but we can't,
                // because `self.medial` is borrowed by `iter`.
                let source = &self.tables.prediction_matrix[postdot.usize()];
                destination.union_with(source);
            }
        }
    }

    fn complete(&mut self, earleme: usize, symbol: Symbol, node: NodeHandle) {
        if self.earley_chart[earleme].predicted.contains(symbol.usize()) {
            self.complete_medial_items(earleme, symbol, node);
            self.complete_unary_predictions(earleme, symbol, node);
            self.complete_binary_predictions(earleme, symbol, node);
        }
    }

    fn complete_medial_items(&mut self, earleme: usize, symbol: Symbol, right_node: NodeHandle) {
        let medial = &self.earley_chart[earleme].medial;

        let inner_start = {
            // we use binary search to narrow down the range of items.
            let set_idx = medial.binary_search_by(|ei| {
                (self.tables.get_rhs1(ei.dot), cmp::Ordering::Greater).cmp(&(Some(symbol), cmp::Ordering::Less))
            });
            match set_idx {
                Ok(idx) | Err(idx) => idx,
            }
        };

        // The range contains items that have the same RHS1 symbol.
        let inner_end = medial[inner_start..]
            .iter()
            .take_while(|ei| self.tables.get_rhs1(ei.dot) == Some(symbol))
            .count();
        for item in &medial[inner_start .. inner_start + inner_end] {
            self.complete.push(CompletedItem {
                dot: item.dot,
                origin: item.origin,
                left_node: item.node,
                right_node: Some(right_node),
            });
        }
    }

    fn complete_unary_predictions(&mut self, earleme: usize, symbol: Symbol, node: NodeHandle) {
        for trans in self.tables.unary_completions(symbol) {
            if self.earley_chart[earleme].predicted.contains(trans.symbol.usize()) {
                // No checks for uniqueness, because `medial` will be deduplicated.
                // from A ::= • B
                // to   A ::=   B •
                self.complete.push(CompletedItem {
                    origin: earleme,
                    dot: trans.dot,
                    left_node: node,
                    right_node: None,
                });
            }
        }
    }

    fn complete_binary_predictions(&mut self, earleme: usize, symbol: Symbol, node: NodeHandle) {
        for trans in self.tables.binary_completions(symbol) {
            if self.earley_chart[earleme].predicted.contains(trans.symbol.usize()) {
                // No checks for uniqueness, because `medial` will be deduplicated.
                // from A ::= • B   C
                // to   A ::=   B • C
                // Where C is terminal or nonterminal.
                self.next_set.medial.push(Item {
                    origin: earleme,
                    dot: trans.dot,
                    node: node,
                });
            }
        }
    }

    fn earleme(&self) -> usize {
        self.earley_chart.len() - 1
    }

    fn finished_node(&self) -> Option<NodeHandle> {
        self.finished_node
    }

    fn log_last_earley_set(&self) {
        let dots = self.dots_for_log(self.earley_chart.last().unwrap());
        for (rule_id, dots) in dots {
            print!("{} ::= ", self.tables.symbol_names[self.tables.get_lhs(rule_id).usize()]);
            if let Some(origins) = dots.get(&0) {
                print!("{:?}", origins);
            }
            print!(" {} ", self.tables.symbol_names[self.tables.get_rhs0(rule_id).unwrap().usize()]);
            if let Some(origins) = dots.get(&1) {
                print!("{:?}", origins);
            }
            if let Some(rhs1) = self.tables.get_rhs1(rule_id) {
                print!(" {} ", self.tables.symbol_names[rhs1.usize()]);
            }
            println!();
        }
        println!();
    }

    fn log_earley_set_diff(&self) {
        let dots_last_by_id = self.dots_for_log(self.earley_chart.last().unwrap());
        let mut dots_next_by_id = self.dots_for_log(&self.next_set);
        let mut rule_ids: BTreeSet<usize> = BTreeSet::new();
        rule_ids.extend(dots_last_by_id.keys());
        rule_ids.extend(dots_next_by_id.keys());
        for item in self.complete.iter() {
            let position = if self.tables.get_rhs1(item.dot).is_some() { 2 } else { 1 };
            dots_next_by_id.entry(item.dot).or_insert(BTreeMap::new()).entry(position).or_insert(BTreeSet::new()).insert(item.origin);
        }
        let mut empty_diff = true;
        for rule_id in rule_ids {
            let dots_last = dots_last_by_id.get(&rule_id);
            let dots_next = dots_next_by_id.get(&rule_id);
            if dots_last == dots_next {
                continue;
            }
            empty_diff = false;
            print!("from {} ::= ", self.tables.symbol_names[self.tables.get_lhs(rule_id).usize()]);
            if let Some(origins) = dots_last.and_then(|d| d.get(&0)) {
                print!("{:?}", origins);
            }
            print!(" {} ", self.tables.symbol_names[self.tables.get_rhs0(rule_id).unwrap().usize()]);
            if let Some(origins) = dots_last.and_then(|d| d.get(&1)) {
                print!("{:?}", origins);
            }
            if let Some(rhs1) = self.tables.get_rhs1(rule_id) {
                print!(" {} ", self.tables.symbol_names[rhs1.usize()]);
            }
            println!();
            print!("to   {} ::= ", self.tables.symbol_names[self.tables.get_lhs(rule_id).usize()]);
            if let Some(origins) = dots_next.and_then(|d| d.get(&0)) {
                print!("{:?}", origins);
            }
            print!(" {} ", self.tables.symbol_names[self.tables.get_rhs0(rule_id).unwrap().usize()]);
            if let Some(origins) = dots_next.and_then(|d| d.get(&1)) {
                print!("{:?}", origins);
            }
            if let Some(rhs1) = self.tables.get_rhs1(rule_id) {
                print!(" {} ", self.tables.symbol_names[rhs1.usize()]);
            }
            if let Some(origins) = dots_next.and_then(|d| d.get(&2)) {
                print!("{:?}", origins);
            }
            println!();
        }
        if empty_diff {
            println!("no diff");
            println!();
        } else {
            println!();
        }
    }

    fn dots_for_log(&self, es: &EarleySet) -> BTreeMap<usize, BTreeMap<usize, BTreeSet<usize>>> {
        let mut dots = BTreeMap::new();
        for (i, rule) in self.tables.rules.iter().enumerate() {
            if es.predicted.contains(rule.lhs.usize()) {
                dots.entry(i).or_insert(BTreeMap::new()).entry(0).or_insert(BTreeSet::new()).insert(self.earleme());
            }
        }
        for item in &es.medial {
            dots.entry(item.dot).or_insert(BTreeMap::new()).entry(1).or_insert(BTreeSet::new()).insert(item.origin);
        }
        dots
    }
}

impl<T> BinaryHeap<T>
    where T: Ord + Copy,
{
    fn new() -> Self {
        Self {
            vec: vec![],
        }
    }

    fn with_capacity(capacity: usize) -> Self {
        Self {
            vec: Vec::with_capacity(capacity),
        }
    }

    fn is_empty(&self) -> bool {
        self.vec.is_empty()
    }

    fn iter(&self) -> impl Iterator<Item=&T> {
        self.vec.iter()
    }

    /// Returns the greatest item in the binary heap, or `None` if it is empty.
    #[inline]
    pub fn peek(&self) -> Option<&T> {
        self.vec.get(0)
    }

    #[inline(always)]
    fn get(&self, idx_idx: usize) -> Option<&T> {
        self.vec.get(idx_idx)
    }

    /// Removes the greatest item from the binary heap and returns it, or `None` if it
    /// is empty.
    pub fn pop(&mut self) -> Option<T> {
        self.vec.pop().map(move |mut item| {
            if !self.vec.is_empty() {
                mem::swap(&mut item, &mut self.vec[0]);
                self.sift_down(0);
            }
            item
        })
    }

    /// Pushes an item onto the binary heap.
    pub fn push(&mut self, item: T) {
        let old_indices_len = self.vec.len();
        self.vec.push(item);
        self.sift_up(0, old_indices_len);
    }

    /// Consumes the `BinaryHeap` and returns a vector in sorted
    /// (ascending) order.
    fn sift_up(&mut self, start: usize, mut pos: usize) {
        let element_idx = self.vec[pos];
        while pos > start {
            let parent = (pos - 1) / 2;
            let parent_idx = self.vec[parent];
            if element_idx <= parent_idx {
                break;
            }
            self.vec[pos] = parent_idx;
            pos = parent;
        }
        self.vec[pos] = element_idx;
    }

    /// Take an element at `pos` and move it down the heap,
    /// while its children are larger.
    fn sift_down_range(&mut self, mut pos: usize, end: usize) {
        let element_idx = self.vec[pos];
        let mut child = 2 * pos + 1;
        while child < end {
            let right = child + 1;
            // compare with the greater of the two children
            if right < end && !(self.get(child).unwrap() > self.get(right).unwrap()) {
                child = right;
            }
            // if we are already in order, stop.
            if element_idx >= *self.get(child).unwrap() {
                break;
            }
            self.vec[pos] = self.vec[child];
            pos = child;
            child = 2 * pos + 1;
        }
        self.vec[pos] = element_idx;
    }

    fn sift_down(&mut self, pos: usize) {
        let len = self.vec.len();
        self.sift_down_range(pos, len);
    }
}

impl Tables {
    fn new(grammar: &BinarizedGrammar) -> Self {
        let mut result = Self {
            prediction_matrix: vec![],
            start_symbol: grammar.start_symbol.expect("unset start symbol"),
            num_syms: grammar.symbol_source.next_symbol.usize(),
            rules: vec![],
            unary_completions: vec![],
            binary_completions: vec![],
            symbol_names: grammar.symbol_source.symbol_names.clone(),
        };
        result.populate(&grammar);
        result
    }

    fn populate(&mut self, grammar: &BinarizedGrammar) {
        self.populate_prediction_matrix(grammar);
        self.populate_rules(grammar);
        self.populate_completions(grammar);
    }

    fn populate_prediction_matrix(&mut self, grammar: &BinarizedGrammar) {
        self.prediction_matrix.resize(self.num_syms, BitSet::with_capacity(self.num_syms));
        for rule in &grammar.rules {
            self.prediction_matrix[rule.lhs.usize()].insert(rule.rhs0.usize());
        }
        self.reflexive_closure();
        self.transitive_closure();
    }

    fn reflexive_closure(&mut self) {
        for i in 0 .. self.num_syms {
            self.prediction_matrix[i].insert(i);
        }
    }

    fn transitive_closure(&mut self) {
        for pos in 0 .. self.num_syms {
            let (rows0, rows1) = self.prediction_matrix.split_at_mut(pos);
            let (rows1, rows2) = rows1.split_at_mut(1);
            for dst_row in rows0.iter_mut().chain(rows2.iter_mut()) {
                if dst_row.contains(pos) {
                    dst_row.union_with(&rows1[0]);
                }
            }
        }
    }

    fn populate_rules(&mut self, grammar: &BinarizedGrammar) {
        self.rules = grammar.rules.clone();
    }

    fn populate_completions(&mut self, grammar: &BinarizedGrammar) {
        self.unary_completions.resize(self.num_syms, vec![]);
        self.binary_completions.resize(self.num_syms, vec![]);
        for (i, rule) in grammar.rules.iter().enumerate() {
            if rule.rhs1.is_some() {
                self.binary_completions[rule.rhs0.usize()].push(PredictionTransition {
                    symbol: rule.lhs,
                    dot: i,
                });
            } else {
                self.unary_completions[rule.rhs0.usize()].push(PredictionTransition {
                    symbol: rule.lhs,
                    dot: i,
                });
            }
        }
    }

    fn get_rhs0(&self, n: usize) -> Option<Symbol> {
        self.rules.get(n).map(|rule| rule.rhs0)
    }

    fn get_rhs1(&self, n: usize) -> Option<Symbol> {
        self.rules.get(n).and_then(|rule| rule.rhs1)
    }

    fn get_rhs1_cmp(&self, dot: usize) -> MaybePostdot {
        match self.rules[dot].rhs1 {
            None => MaybePostdot::Unary,
            Some(rhs1) => MaybePostdot::Binary(rhs1),
        }
    }

    fn get_lhs(&self, n: usize) -> Symbol {
        self.rules[n].lhs
    }

    fn unary_completions(&self, symbol: Symbol) -> &[PredictionTransition] {
        &self.unary_completions[symbol.usize()][..]
    }

    fn binary_completions(&self, symbol: Symbol) -> &[PredictionTransition] {
        &self.binary_completions[symbol.usize()][..]
    }
}

impl Forest {
    fn new(grammar: &BinarizedGrammar) -> Self {
        Self {
            graph: vec![],
            summands: vec![],
            eval: grammar.rules.iter().map(|rule| rule.source).collect(),
        }
    }

    fn leaf(&mut self, terminal: Symbol, _x: usize, values: u32) -> NodeHandle {
        let handle = NodeHandle(self.graph.len());
        self.graph.push(Node::Leaf {
            terminal,
            values,
        });
        handle
    }

    fn push_summand(&mut self, item: CompletedItem) {
        self.summands.push(Product {
            action: self.get_eval(item.dot).unwrap_or(NULL_ACTION),
            left_factor: item.left_node,
            right_factor: item.right_node,
        });
    }

    fn sum(&mut self, _lhs_sym: Symbol, _origin: usize) -> NodeHandle {
        let handle = NodeHandle(self.graph.len());
        self.graph.push(Node::Sum {
            summands: mem::replace(&mut self.summands, vec![]),
        });
        handle
    }

    fn get_eval(&self, dot: usize) -> Option<u32> {
        self.eval[dot].map(|id| id as u32)
    }
}

struct Evaluator<F, G> {
    eval_product: F,
    eval_leaf: G,
}

impl<T, F, G> Evaluator<F, G>
    where F: Fn(u32, &[T]) -> T + Copy,
          G: Fn(Symbol, u32) -> T + Copy,
          T: Clone + ::std::fmt::Debug
{
    fn new(eval_product: F, eval_leaf: G) -> Self {
        Self {
            eval_product,
            eval_leaf,
        }
    }

    fn evaluate(&mut self, forest: &mut Forest, finished_node: NodeHandle) -> T {
        self.evaluate_rec(forest, finished_node)[0].clone()
    }

    fn evaluate_rec(&mut self, forest: &mut Forest, handle: NodeHandle) -> Vec<T> {
        match &forest.graph[handle.0] {
            &Node::Sum { ref summands, .. } => {
                assert_eq!(summands.len(), 1);
                let product = summands[0];
                let mut result = self.evaluate_rec(forest, product.left_factor);
                if let Some(factor) = product.right_factor {
                    let v = self.evaluate_rec(forest, factor);
                    result.extend(v);
                }
                if product.action != NULL_ACTION {
                    vec![(self.eval_product)(product.action as u32, &result[..])]
                } else {
                    result
                }
            }
            &Node::Leaf { terminal, values } => {
                vec![(self.eval_leaf)(terminal, values)]
            }
        }
    }
}

#[derive(Clone, Debug)]
enum Value {
    Digits(String),
    Float(f64),
    None,
}

fn calc(expr: &str) -> f64 {
    let mut grammar = Grammar::new();
    let sum = grammar.make_symbol("sum");
    let factor = grammar.make_symbol("factor");
    let op_mul = grammar.make_symbol("op_mul");
    let op_div = grammar.make_symbol("op_div");
    let lparen = grammar.make_symbol("lparen");
    let rparen = grammar.make_symbol("rparen");
    let expr_sym = grammar.make_symbol("expr_sym");
    let op_minus = grammar.make_symbol("op_minus");
    let op_plus = grammar.make_symbol("op_plus");
    let number = grammar.make_symbol("number");
    let whole = grammar.make_symbol("whole");
    let digit = grammar.make_symbol("digit");
    let dot = grammar.make_symbol("dot");
    // sum ::= sum [+-] factor
    // sum ::= factor
    // factor ::= factor [*/] expr
    // factor ::= expr
    // expr ::= '(' sum ')' | '-' expr | number
    // number ::= whole | whole '.' whole
    // whole ::= whole [0-9] | [0-9]
    grammar.rule(sum).rhs([sum, op_plus, factor]).id(0).build();
    grammar.rule(sum).rhs([sum, op_minus, factor]).id(1).build();
    grammar.rule(sum).rhs([factor]).id(2).build();
    grammar.rule(factor).rhs([factor, op_mul, expr_sym]).id(3).build();
    grammar.rule(factor).rhs([factor, op_div, expr_sym]).id(4).build();
    grammar.rule(factor).rhs([expr_sym]).id(5).build();
    grammar.rule(expr_sym).rhs([lparen, sum, rparen]).id(6).build();
    grammar.rule(expr_sym).rhs([op_minus, expr_sym]).id(7).build();
    grammar.rule(expr_sym).rhs([number]).id(8).build();
    grammar.rule(number).rhs([whole]).id(9).build();
    grammar.rule(number).rhs([whole, dot, whole]).id(10).build();
    grammar.rule(whole).rhs([whole, digit]).id(11).build();
    grammar.rule(whole).rhs([digit]).id(12).build();
    grammar.start_symbol(sum);
    let binarized_grammar = grammar.binarize();
    let mut recognizer = Recognizer::new(binarized_grammar);
    for (i, ch) in expr.chars().enumerate() {
        let terminal = match ch {
            '-' => op_minus,
            '.' => dot,
            '0' ..= '9' => digit,
            '(' => lparen,
            ')' => rparen,
            '*' => op_mul,
            '/' => op_div,
            '+' => op_plus,
            ' ' => continue,
            other => panic!("invalid character {}", other)
        };
        recognizer.begin_earleme();
        recognizer.scan(terminal, ch as u32);
        assert!(recognizer.end_earleme(), "parse failed at character {}", i);
    }
    let finished_node = recognizer.finished_node().expect("parse failed");
    let mut evaluator = Evaluator::new(
        |rule_id, args: &[Value]| {
            match (
                rule_id,
                args.get(0).cloned().unwrap_or(Value::None),
                args.get(1).cloned().unwrap_or(Value::None),
                args.get(2).cloned().unwrap_or(Value::None),
            ) {
                (0, Value::Float(left), _, Value::Float(right)) => {
                    Value::Float(left + right)
                }
                (1, Value::Float(left), _, Value::Float(right)) => {
                    Value::Float(left - right)
                }
                (2, val, Value::None, Value::None) => {
                    val
                }
                (3, Value::Float(left), _, Value::Float(right)) => {
                    Value::Float(left * right)
                }
                (4, Value::Float(left), _, Value::Float(right)) => {
                    Value::Float(left / right)
                }
                (5, val, Value::None, Value::None) => {
                    val
                }
                (6, _, val, _) => {
                    val
                }
                (7, _, Value::Float(num), Value::None) => {
                    Value::Float(-num)
                }
                (8, Value::Digits(digits), Value::None, Value::None) => {
                    Value::Float(digits.parse::<f64>().unwrap())
                }
                (9, val @ Value::Digits(..), _, _) => {
                    val
                }
                (10, Value::Digits(before_dot), _, Value::Digits(after_dot)) => {
                    let mut digits = before_dot;
                    digits.push('.');
                    digits.push_str(&after_dot[..]);
                    Value::Digits(digits)
                }
                (11, Value::Digits(mut num), Value::Digits(digit), _) => {
                    num.push_str(&digit[..]);
                    Value::Digits(num)
                }
                (12, val @ Value::Digits(..), _, _) => {
                    val
                }
                other => panic!("unknown rule id {:?} or args {:?}", rule_id, args)
            }
        },
        |terminal, values| {
            if terminal == digit {
                Value::Digits((values as u8 as char).to_string())
            } else {
                Value::None
            }
        }
    );
    let result = evaluator.evaluate(&mut recognizer.forest, finished_node);
    if let Value::Float(num) = result {
        num
    } else {
        panic!("evaluation failed")
    }
}
___________________________________________________________________________________
use std::iter::Peekable;

const DIGITS_DOT: [char; 11] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'];

fn calc(expr: &str) -> f64 {
    let expr = tokenize(expr);
    let expr = simplify_minus(expr);
    let expr = parse(&mut expr.into_iter().peekable()).unwrap();

    expr.eval()
}

fn tokenize(expr: &str) -> Vec<Token> {
    let mut math = vec![];
    let mut expr = expr.chars().peekable();
    let mut have_to_next;

    while let Some(character) = expr.peek() {
        have_to_next = true;

        match character {
            '+' => math.push(Token::Plus),
            '-' => math.push(Token::Minus),
            '*' => math.push(Token::Star),
            '/' => math.push(Token::Slash),
            '(' => math.push(Token::OpenBrack),
            ')' => math.push(Token::CloseBrack),
            '0'..='9' => {
                math.push(tokenize_number(&mut expr).unwrap());
                have_to_next = false;
            }
            _ => (),
        }

        if have_to_next {
            expr.next();
        }
    }

    math
}

fn tokenize_number<I: Iterator<Item = char>>(expr: &mut Peekable<I>) -> Option<Token> {
    let mut string = String::new();

    match expr.peek() {
        Some(c) if DIGITS_DOT.contains(c) => (),
        _ => return None,
    }

    while let Some(character) = expr.peek() { 
        if DIGITS_DOT.contains(character) {
            string.push(expr.next().unwrap())
        } else {
            break;
        }
    }

    string.parse::<f64>().ok().map(Token::Number)
}

fn simplify_minus(mut expr: Vec<Token>) -> Vec<Token> {
    let mut index_to_make_plus = vec![];
    let mut index_to_remove = vec![];

    let mut is_a_start = true;
    let mut precedent = Prec::Other;

    for (i, t) in expr.iter_mut().enumerate() {
        match t {
            Token::Minus => match precedent {
                Prec::Minus => {
                    index_to_remove.push(i - 1);
                    *t = Token::Plus;
                    precedent = Prec::Other;
                }
                Prec::Plus => index_to_remove.push(i - 1),
                Prec::Other => precedent = Prec::Minus,
            },
            Token::Plus => {
                match precedent {
                    Prec::Minus => index_to_remove.push(i),
                    _ => precedent = Prec::Plus,
                }
                is_a_start = false;
            }
            Token::Number(ref mut x) => {
                if matches!(precedent, Prec::Minus) {
                    *x = -*x;
                    if is_a_start {
                        index_to_remove.push(i - 1);
                    } else {
                        index_to_make_plus.push(i - 1);
                    }
                }
                is_a_start = false;
                precedent = Prec::Other
            }
            Token::OpenBrack | Token::Star | Token::Slash => {
                precedent = Prec::Other;
                is_a_start = true
            }
            _ => {
                precedent = Prec::Other;
                is_a_start = false
            }
        }
    }

    for i in index_to_make_plus {
        expr[i] = Token::Plus;
    }

    for i in index_to_remove.into_iter().rev() {
        expr.remove(i);
    }

    expr
}

fn parse<I: Iterator<Item = Token>>(expr: &mut Peekable<I>) -> Option<Expr> {
    let mut x = Expr::zero();

    while let Some(op) = expr.peek() {
        x = match op {
            Token::Plus => add(x, expr).unwrap(),
            Token::Star => mul(x, expr).unwrap(),
            Token::Slash => div(x, expr).unwrap(),
            Token::OpenBrack => brack(expr).unwrap(),
            Token::Minus => sub(x, expr).unwrap(),
            Token::Number(_) => Expr::Number(expr.next().unwrap().into_value()),
            _ => unreachable!(),
        }
    }

    Some(x)
}

fn get_until_sum<I: Iterator<Item = Token>>(expr: &mut Peekable<I>) -> Option<Expr> {
    let mut x = Expr::zero();

    while let Some(op) = expr.peek() {
        x = match op {
            Token::Plus | Token::Minus => break,
            Token::Star => mul(x, expr).unwrap(),
            Token::Slash => div(x, expr).unwrap(),
            Token::OpenBrack => brack(expr).unwrap(),
            Token::Number(_) => Expr::Number(expr.next().unwrap().into_value()),
            _ => unreachable!(),
        }
    }

    Some(x)
}

fn brack<I: Iterator<Item = Token>>(expr: &mut Peekable<I>) -> Option<Expr> {
    match expr.peek() {
        Some(c) if matches!(c, Token::OpenBrack) => expr.next(),
        _ => return None,
    };

    let mut inner_expr = vec![];
    let mut deep = 0;

    loop {
        let token = if let Some(t) = expr.peek() {
            t
        } else {
            break None;
        };

        match token {
            Token::OpenBrack => {
                deep += 1;
                inner_expr.push(expr.next().unwrap())
            }
            Token::Number(_) | Token::Plus | Token::Star | Token::Slash | Token::Minus => {
                inner_expr.push(expr.next().unwrap())
            }
            Token::CloseBrack => {
                if deep == 0 {
                    expr.next();

                    break Some(Expr::Group(Box::new(
                        parse(&mut inner_expr.into_iter().peekable()).unwrap(),
                    )));
                } else {
                    deep -= 1;
                    inner_expr.push(expr.next().unwrap())
                }
            }
        }
    }
}

fn get_next_x<I: Iterator<Item = Token>>(expr: &mut Peekable<I>) -> Option<Expr> {
    let token = expr.peek()?;

    match token {
        Token::Number(_) => Some(Expr::Number(expr.next().unwrap().into_value())),
        Token::OpenBrack => brack(expr),
        Token::Minus => {
            expr.next();
            Some(Expr::Opposed(Box::new(brack(expr).unwrap())))
        }
        _ => panic!(),
    }
}

fn add<I: Iterator<Item = Token>>(x: Expr, expr: &mut Peekable<I>) -> Option<Expr> {
    match expr.peek() {
        Some(c) if matches!(c, Token::Plus) => expr.next(),
        _ => return None,
    };

    Some(Expr::Add(Box::new(x), Box::new(parse(expr).unwrap())))
}

fn sub<I: Iterator<Item = Token>>(x: Expr, expr: &mut Peekable<I>) -> Option<Expr> {
    match expr.peek() {
        Some(c) if matches!(c, Token::Minus) => expr.next(),
        _ => return None,
    };

    Some(Expr::Sub(
        Box::new(x),
        Box::new(get_until_sum(expr).unwrap()),
    ))
}

fn mul<I: Iterator<Item = Token>>(x: Expr, expr: &mut Peekable<I>) -> Option<Expr> {
    match expr.peek() {
        Some(c) if matches!(c, Token::Star) => expr.next(),
        _ => return None,
    };

    Some(Expr::Mul(Box::new(x), Box::new(get_next_x(expr).unwrap())))
}

fn div<I: Iterator<Item = Token>>(x: Expr, expr: &mut Peekable<I>) -> Option<Expr> {
    match expr.peek() {
        Some(c) if matches!(c, Token::Slash) => expr.next(),
        _ => return None,
    };

    Some(Expr::Div(Box::new(x), Box::new(get_next_x(expr).unwrap())))
}

#[derive(PartialEq)]
enum Token {
    Number(f64),
    Plus,
    Minus,
    Star,
    Slash,
    OpenBrack,
    CloseBrack,
}

impl Token {
    fn into_value(self) -> f64 {
        match self {
            Self::Number(x) => x,
            _ => panic!(),
        }
    }
}

enum Expr {
    Number(f64),
    Add(Box<Expr>, Box<Expr>),
    Sub(Box<Expr>, Box<Expr>),
    Mul(Box<Expr>, Box<Expr>),
    Div(Box<Expr>, Box<Expr>),
    Opposed(Box<Expr>),
    Group(Box<Expr>),
}

impl Expr {
    fn eval(self) -> f64 {
        match self {
            Self::Number(x) => x,
            Self::Add(x, y) => (*x).eval() + (*y).eval(),
            Self::Sub(x, y) => (*x).eval() - (*y).eval(),
            Self::Mul(x, y) => (*x).eval() * (*y).eval(),
            Self::Div(x, y) => (*x).eval() / (*y).eval(),
            Self::Opposed(x) => -(*x).eval(),
            Self::Group(x) => (*x).eval(),
        }
    }

    fn zero() -> Self {
        Self::Number(0.)
    }
}

enum Prec {
    Plus,
    Minus,
    Other,
}
__________________________________________________________
use std::iter::once;

#[derive(Debug, PartialEq, Clone, Copy)]
enum Symbol {
    Number(f64),
    Addition,
    Subtraction,
    Multiplication,
    Division,
    PrenL,
    PrenR,
}

fn calc(expr: &str) -> f64 {
    let symbols = parse_symbols(expr);
    let number = parse_symbols_to_number(&symbols);
    if let Symbol::Number(n) = number {
        return n;
    } else {
        panic!();
    }
}

fn parse_symbols_to_number(input: &[Symbol]) -> Symbol {
    if input.is_empty() {
        return Symbol::Number(0.0);
    }
    let mut parenthesis = Vec::new();
    let mut stack = Vec::new();
    for s in once(&Symbol::PrenL)
        .chain(input.iter())
        .chain(once(&Symbol::PrenR))
    {
        match s {
            // no parenthesis -> don't care
            Symbol::Number(_)
            | Symbol::Addition
            | Symbol::Subtraction
            | Symbol::Multiplication
            | Symbol::Division => stack.push(*s),

            // opening new scope -> keep index of it
            Symbol::PrenL => parenthesis.push(stack.len()),

            // closing a scope -> have to deal with it
            Symbol::PrenR => {
                let opening_paren_index = parenthesis.pop().unwrap();
                let input: Vec<Symbol> = stack.drain(opening_paren_index..).collect();

                // punkt vor strich ;)
                let new_expr = strich(&punkt(&input));
                stack.push(new_expr);
            }
        }
    }
    assert_eq!(stack.len(), 1);
    assert!(parenthesis.is_empty());
    stack.pop().unwrap()
}

fn punkt(input: &[Symbol]) -> Vec<Symbol> {
    println!("punkt({:?})", input);
    let mut todo: Option<Symbol> = None;
    let mut stack: Vec<Symbol> = Vec::new();
    for s in input {
        println!("stack:{:?}, s:{:?}, todo:{:?}", stack, s, todo);
        match (todo, s) {
            // nothing to do
            (None, Symbol::Multiplication | Symbol::Division) => todo = Some(*s),
            (None, Symbol::Number(_) | Symbol::Addition | Symbol::Subtraction) => stack.push(*s),

            // something todo
            (Some(Symbol::Multiplication), Symbol::Number(n2)) => {
                match stack.pop() {
                    Some(Symbol::Number(n1)) => stack.push(Symbol::Number(n1 * n2)),
                    _ => unreachable!(),
                };
                todo = None;
            }
            (Some(Symbol::Division), Symbol::Number(n2)) => {
                match stack.pop() {
                    Some(Symbol::Number(n1)) => stack.push(Symbol::Number(n1 / n2)),
                    _ => unreachable!(),
                };
                todo = None;
            }
            // now this is mean: if we have to multiply or divide by a negative number: we take the '-' and push it the left of the '*' or '/'
            (Some(_), Symbol::Subtraction) => {
                let num = stack.pop().unwrap();
                stack.push(*s);
                stack.push(num);
            }
            _ => unreachable!(),
        }
    }
    println!("  > {:?}", stack);
    stack
}

fn strich(input: &[Symbol]) -> Symbol {
    println!("strich({:?})", input);
    let mut todo: Option<Symbol> = None;
    let mut stack: Vec<Symbol> = Vec::new();
    for s in input {
        println!("stack:{:?}, s:{:?}, todo:{:?}", stack, s, todo);
        match (todo, s) {
            // nothing todo
            (None, Symbol::Addition | Symbol::Subtraction) => todo = Some(*s),
            (None, Symbol::Number(_)) => stack.push(*s),

            // we have something to do from before
            (Some(Symbol::Addition), Symbol::Number(n2)) => {
                match stack.pop() {
                    Some(Symbol::Number(n1)) => stack.push(Symbol::Number(n1 + n2)),
                    None => stack.push(Symbol::Number(*n2)),
                    _ => unreachable!(),
                };
                todo = None;
            }
            (Some(Symbol::Subtraction), Symbol::Number(n2)) => {
                match stack.pop() {
                    Some(Symbol::Number(n1)) => stack.push(Symbol::Number(n1 - n2)),
                    None => stack.push(Symbol::Number(-n2)),
                    _ => unreachable!(),
                };
                todo = None;
            }

            // we are already in a addition/subtraction, but additional unary '-' pop up
            // so we have to negate the current todo
            (Some(Symbol::Addition), Symbol::Subtraction) => todo = Some(Symbol::Subtraction),
            (Some(Symbol::Subtraction), Symbol::Subtraction) => todo = Some(Symbol::Addition),

            // else: panic! this should not happen
            _ => unreachable!(),
        }
    }
    assert_eq!(stack.len(), 1);
    println!("  > {:?}", stack);
    stack.pop().unwrap()
}

fn parse_symbols(expr: &str) -> Vec<Symbol> {
    let expr = expr.replace(" ", "");
    let mut result: Vec<Symbol> = Vec::new();
    let mut number_string = String::new();
    for c in expr.chars() {
        match c {
            '0'..='9' | '.' => number_string.push(c),
            _ => {
                if !number_string.is_empty() {
                    result.push(Symbol::Number(number_string.parse().unwrap()));
                    number_string.clear();
                }
                match c {
                    '+' => result.push(Symbol::Addition),
                    '-' => result.push(Symbol::Subtraction),
                    '*' => result.push(Symbol::Multiplication),
                    '/' => result.push(Symbol::Division),
                    '(' => result.push(Symbol::PrenL),
                    ')' => result.push(Symbol::PrenR),
                    _ => unreachable!(),
                };
            }
        };
    }
    if !number_string.is_empty() {
        result.push(Symbol::Number(number_string.parse().unwrap()));
    }
    result
}
