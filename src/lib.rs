use pyo3::prelude::*;

const NUMERALS: [(&str, u32); 13] = [
    ("M", 1000),
    ("CM", 900),
    ("D", 500),
    ("CD", 400),
    ("C", 100),
    ("XC", 90),
    ("L", 50),
    ("XL", 40),
    ("X", 10),
    ("IX", 9),
    ("V", 5),
    ("IV", 4),
    ("I", 1),
];

pub fn to_roman(mut value: u32) -> String {
    if value == 0 {
        return "N".to_owned();
    }
    let mut output = String::with_capacity(16);
    for (numeral, integer) in NUMERALS {
        while value >= integer {
            output.push_str(numeral);
            value -= integer;
        }
    }
    output
}

pub fn from_valid_roman(value: &str) -> u32 {
    let value = value.strip_suffix('\n').unwrap_or(value);
    let mut result = 0;
    let mut rest = value;
    for (numeral, integer) in NUMERALS {
        while let Some(next) = rest.strip_prefix(numeral) {
            result += integer;
            rest = next;
        }
    }
    result
}

#[pyfunction]
fn _to_roman(value: u32) -> String {
    to_roman(value)
}

#[pyfunction]
fn _from_roman(value: &str) -> u32 {
    from_valid_roman(value)
}

#[pymodule]
fn _native(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(_to_roman, module)?)?;
    module.add_function(wrap_pyfunction!(_from_roman, module)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::{from_valid_roman, to_roman};

    #[test]
    fn frozen_examples() {
        let examples = [
            (0, "N"),
            (1, "I"),
            (4, "IV"),
            (9, "IX"),
            (49, "XLIX"),
            (972, "CMLXXII"),
            (4_999, "MMMMCMXCIX"),
        ];
        for (value, numeral) in examples {
            assert_eq!(to_roman(value), numeral);
            if value > 0 {
                assert_eq!(from_valid_roman(numeral), value);
            }
        }
    }

    #[test]
    fn complete_round_trip() {
        for value in 1..5_000 {
            let numeral = to_roman(value);
            assert_eq!(from_valid_roman(&numeral), value);
        }
    }

    #[test]
    fn preserves_single_lf_boundary() {
        assert_eq!(from_valid_roman("I\n"), 1);
        assert_eq!(from_valid_roman("\n"), 0);
    }
}
